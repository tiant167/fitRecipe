#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: chaihaotian
# @Date:   2015-04-26 15:44:45
# @Last Modified by:   chaihaotian
# @Last Modified time: 2015-07-25 16:47:11
from django.db.models import Prefetch
from django.db.models import Q
from base.views import BaseView
from .models import Recipe, Ingredient
from accounts.models import Account
from collection.models import RecipeCollection
from .serializers import RecipeSerializer, IngredientSerializer
from comment.serializers import CommentSerializer
from label.models import Label
from fitrecipe.utils import pick_data
# Create your views here.

class RecipeList(BaseView):

    def get(self, request, format=None):
        '''
        List all recipes

        labels=1,2,3,4&start=10&num=10&order
        '''
        labels = request.GET.get('labels', None)
        start = request.GET.get('start', '0')
        num = request.GET.get('num', '10')
        order = request.GET.get('order', 'calories')
        desc = request.GET.get('desc', 'false')
        # https://docs.djangoproject.com/en/1.8/ref/models/querysets/#when-querysets-are-evaluated
        recipes = Recipe.get_recipe_list(labels, order, desc, start, num)
        serializer = RecipeSerializer(recipes, many=True)
        return self.success_response(serializer.data)


class RecipeUpdateList(BaseView):
    def get(self, request, format=None):
        start = abs(int(request.GET.get('start', 0)))
        num = abs(int(request.GET.get('num', 10)))
        return self.success_response(RecipeSerializer(Recipe.get_latest_recipe(start=start, num=num), many=True).data)


class RecipeDetail(BaseView):
    def get(self, request, pk, format=None):
        '''
        return a specific recipe.
        '''
        recipe = Recipe.objects.select_related('author').get(pk=pk)
        try:
            user = Account.find_account_by_user(request.user)
            has_collected = RecipeCollection.has_collected(recipe, user)
        except Account.DoesNotExist:
            has_collected = (False, -1)
        if recipe.status > 0:
            serializer = RecipeSerializer(recipe, context={'simple': False})
            result = serializer.data
            result['has_collected'], result['collect_id'] = has_collected
            result['comment_set'] = CommentSerializer(recipe.comment_set.order_by('-created_time')[0:20], many=True).data
            result['comment_count'] = recipe.comment_set.count()
            return self.success_response(result)
        else:
            return self.fail_response(400, 'DoesNotExist')


class RecipeSearch(BaseView):
    def get(self, request, format=None):
        '''
        search
        '''
        keyword = request.GET.get('keyword', None)
        start = abs(int(request.GET.get('start', 0)))
        num = abs(int(request.GET.get('num', 10)))
        if keyword is None:
            return self.success_response([])
        r = Recipe.objects.filter(Q(status__gt=0) & (Q(title__contains=keyword) | Q(label__name__contains=keyword)))
        return self.success_response(RecipeSerializer(r[start: start + num], many=True).data)


class IngredientSearch(BaseView):
    def get(self, request, format=None):
        '''
        ingredient search
        '''
        keyword = request.GET.get('keyword', None)
        start = abs(int(request.GET.get('start', 0)))
        num = abs(int(request.GET.get('num', 10)))
        if keyword is None:
            return self.success_response([])
        ingredients = Ingredient.objects.filter(name__contains=keyword)
        return self.success_response(IngredientSerializer(ingredients, many=True).data)


class FoodSearch(BaseView):
    def get(self, request, format=None):
        '''
        ingredient search
        '''
        keyword = request.GET.get('keyword', None)
        start = abs(int(request.GET.get('start', 0)))
        num = abs(int(request.GET.get('num', 10)))
        if keyword is None:
            return self.success_response([])
        r = Recipe.objects.filter(status__gt=0, title__contains=keyword)
        i = Ingredient.objects.filter(name__contains=keyword)
        result = pick_data(r, 1) + pick_data(i, 0)
        return self.success_response(result[start: start + num])
