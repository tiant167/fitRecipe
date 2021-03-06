#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.db import IntegrityError
from base.views import BaseView
from .models import Plan, Calendar, Punch
from recipe.models import Recipe, Ingredient
from .serializers import PlanSerializer, CalendarSerializer, PunchSerializer
from accounts.models import Account
from datetime import date, datetime
from collection.models import RecipeCollection
# Create your views here.
class PlanList(BaseView):

    def get(self, request, format=None):
        '''
        List all plans in simple mode
        '''
        plans = Plan.objects.filter(is_personal=False)
        serializer = PlanSerializer(plans, many=True)
        return self.success_response(serializer.data)

    def post(self, request, format=None):
        '''
        create a personal plan
        {
            "id": 18,
            "dish": [{
                "type": 0,
                "ingredient": [{
                    "id": 1,
                    "amount": 100
                }],
                "recipe": [{
                    "id": 2,
                    "amount": 200
                }]
            },{
                "type": 1,
                "ingredient": [],
                "recipe": [{
                    "id":3,
                    "amount": 300
                }]
            }],
            "joined_date": "2015-01-01"
        }
        '''
        try:
            body = json.loads(request.body)
            user = Account.find_account_by_user(request.user)
            try:
                joined_date = datetime.strptime(body['joined_date'],'%Y-%m-%d').date()
            except:
                joined_date = date.today()
            planid = body.get('id', None)
            routines = [{'video': None, 'dish': body.get('dish', [])}]
            if planid is None:
                # create
                p = Plan.objects.create(user=user, routines= json.dumps(routines))
            else :
                p = Plan.objects.get(user=user, pk=planid)
                p.routines = json.dumps(routines)
                p.save()
            # after created it join it!
            try:
                c = Calendar.objects.get(user=user, joined_date=joined_date)
                if c.plan.id != p.id:
                    c.plan = p
                    c.save()
            except Calendar.DoesNotExist:
                Calendar.objects.create(user=user, plan=p, joined_date=joined_date)
            # delete todays punch
            Punch.objects.filter(user=user, date=date.today()).update(state=-10)
            return self.success_response(PlanSerializer(p).data)
        except:
            raise#return self.fail_response(400, 'fail')


class PlanDetail(BaseView):

    def get(self, request, plan_id, format=None):
        '''
        get detail info
        '''
        plan = Plan.objects.get(pk=plan_id)
        serializer = PlanSerializer(plan, context={'simple': False})
        return self.success_response(serializer.data)


class CalendarList(BaseView):

    def get(self, request, format=None):
        '''
        get my calendar
        '''
        user = Account.find_account_by_user(request.user)
        turn_to_date = lambda x: x and datetime.strptime(x, '%Y%m%d') or date.today()
        start_date = turn_to_date(request.GET.get('start', None))
        end_date = turn_to_date(request.GET.get('end', None))
        plans = []
        calendars = (Calendar.objects
            .select_related('plan')
            .select_related('user')
            .filter(user=user, joined_date__gte=start_date, joined_date__lte=end_date))

        try:
            last_joined = Calendar.objects.filter(user=user, joined_date__lte=start_date).order_by('-joined_date')[0]
            last = CalendarSerializer(last_joined, context={'simple': False}).data
            plans.append(last['plan'])
        except IndexError:
            last = None
        serializer = CalendarSerializer(calendars, many=True, context={'simple': False}).data
        for c in serializer:
            plans.append(c['plan'])
        punchs = Punch.objects.filter(user=user, date__lte=end_date, date__gte=start_date, state__gte=10)
        count = Punch.objects.filter(user=user, state__gte=10)
        result = {
            'lastJoined': last,
            'calendar': serializer,
            'punch': PunchSerializer(punchs, many=True).data,
            'plans': plans,
            'count': len(count)
        }
        return self.success_response(result)

    def post(self, request, format=None):
        '''
        join plan
        same date & user will use the last one
        {
            "plan": 2,
            "joined_date": "2015-01-01"
        }
        '''
        body = json.loads(request.body)
        plan_id = body.get('plan', None)
        try:
            joined_date = datetime.strptime(body['joined_date'],'%Y-%m-%d').date()
        except:
            joined_date = date.today()
        user = Account.find_account_by_user(request.user)
        if plan_id is None:
            return self.fail_response(400, 'No Plan')
        try:
            p = Plan.objects.get(pk=plan_id)
            p.dish_headcount += 1
            p.save()
        except Plan.DoesNotExist:
            return self.fail_response(400, 'Plan Not Exist')
        try:
            c = Calendar.objects.create(user=user, plan=p, joined_date=joined_date)
        except IntegrityError:
            # existed today
            c = Calendar.objects.get(user=user, joined_date=joined_date)
            c.plan = p
            c.save()
        if not p.is_personal:
            # official plan should clean all plan after
            Calendar.objects.filter(user=user, joined_date__gt=joined_date).delete()
        # join should clean punch of today
        Punch.objects.filter(user=user, date=date.today()).update(state=-10)
        return self.success_response('ok')


class LastPlan(BaseView):
    '''
    获取最后一个
    '''
    def get(self, request, format=None):
        user = Account.find_account_by_user(request.user)
        try:
            c = Calendar.objects.filter(user=user, joined_date__lte=date.today()).order_by('-joined_date')[0]
            return self.success_response(CalendarSerializer(c).data)
        except IndexError:
            # new user has no plan
            return self.success_response({})


class PunchSize(BaseView):
    '''
    docstring for PunchSize
    '''
    def get(self, request, format=None):
        user = Account.find_account_by_user(request.user)
        count_punch = Punch.objects.filter(user=user, state__gte=10).count()
        count_recipe = RecipeCollection.objects.filter(owner=user, status__gte=0).count()
        return self.success_response({'count': count_punch, 'recipe': count_recipe})


class PunchList(BaseView):
    '''
    打卡
    '''
    def get(self, request, format=None):
        def get_planid(punch, calendar_list):
            temp_storage = None
            for c in calendar_list:
                if punch.date > c['joined_date']:
                    day = punch.date - c['joined_date']
                    return (c['plan'], day.days)
                elif punch.date == c['joined_date']:
                    return (c['plan'], 1)
                else:
                    temp_storage = None
            return (None, 0)

        user = Account.find_account_by_user(request.user)
        turn_to_date = lambda x: x and datetime.strptime(x, '%Y%m%d') or date.today()
        start_date = turn_to_date(request.GET.get('start', None))
        end_date = turn_to_date(request.GET.get('end', None))
        punchs = Punch.objects.filter(user=user, date__lte=end_date, date__gte=start_date, state__gte=10)
        calendars = Calendar.objects.filter(user=user, joined_date__lte=end_date, joined_date__gte=start_date).order_by('joined_date') # asc
        # get all calendar
        try:
            last_calendar = Calendar.objects.filter(user=user, joined_date__lte=start_date).order_by('-joined_date')[0]
            calendar_list = [{'joined_date': last_calendar.joined_date, 'plan': last_calendar.plan.id}]
        except IndexError:
            calendar_list = []
        for c in calendars:
            calendar_list.append({'joined_date': c.joined_date, 'plan': c.plan.id})
        result = []
        calendar_list.reverse()
        for p in punchs:
            planid, day = get_planid(p, calendar_list)
            plan = Plan.objects.get(pk=planid)
            current_day_count = day % plan.total_days
            if current_day_count == 0:
                current_day_count = plan.total_days
            # 从1开始计数的
            dish = json.loads(plan.routines)[current_day_count-1]['dish']
            p_json = PunchSerializer(p).data
            p_json['dish'] = [item for item in dish if item['type'] == p.type]
            result.append(p_json)
        count = Punch.objects.filter(user=user, state__gte=10).count()
        return self.success_response({'punchs': result, 'count': count})

    def post(self, request, format=None):
        user = Account.find_account_by_user(request.user)
        body = json.loads(request.body)
        type = body.get('type', None)
        img = body.get('img', None)
        if None in (type, img):
            return self.fail_response(400, 'Wrong Data')
        p = Punch.objects.create(user=user, type=type, img=img)
        return self.success_response(PunchSerializer(p).data)


class DeletePunch(BaseView):
    def post(self, request, punch_id, format=None):
        user = Account.find_account_by_user(request.user)
        try:
            p = Punch.objects.get(user=user, pk=punch_id)
            p.state = -10
            p.save()
            return self.success_response('ok')
        except Punch.DoesNotExist:
            return self.fail_response(404, 'No Punch')


class PlanListAndCurrent(BaseView):
    def get(self, request, format=None):
        '''
        List all plans in simple mode
        '''
        plans = Plan.objects.filter(is_personal=False)
        serializer = PlanSerializer(plans, many=True)
        user = Account.find_account_by_user(request.user)
        try:
            c = Calendar.objects.filter(user=user, joined_date__lte=date.today()).order_by('-joined_date')[0]
            current = CalendarSerializer(c).data
        except IndexError:
            # new user no plan
            current = {}
        result = {
            'plans': serializer.data,
            'current': current
        }
        return self.success_response(result)

