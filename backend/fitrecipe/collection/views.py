#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.db import IntegrityError
from django.db.models import ObjectDoesNotExist

from base.views import BaseView, AuthView
from accounts.models import Account
from article.models import Series
from theme.models import Theme
from recipe.models import Recipe
from .models import ThemeCollection, SeriesCollection, RecipeCollection
from .serializers import RecipeCollectionSerializer, ThemeCollectionSerializer, SeriesCollectionSerializer


class CollectionCreate(AuthView):
    def post(self, request, format=None):
        try:
            data = json.loads(request.body)
            collection_id = data['id']
            collection_type = data['type']
        except:
            return self.fail_response(400, 'BadArgumrent')
        try:
            if collection_type == 'theme':
                model = ThemeCollection
                obj = Theme.objects.get(pk=collection_id)
                serializer = ThemeCollectionSerializer
            elif collection_type == 'series':
                model = SeriesCollection
                obj = Series.objects.get(pk=collection_id)
                serializer = SeriesCollectionSerializer
            elif collection_type == 'recipe':
                obj = Recipe.objects.get(pk=collection_id)
                model = RecipeCollection
                serializer = RecipeCollectionSerializer
            else:
                return self.fail_response(400, 'BadArgument')
        except ObjectDoesNotExist:
            return self.fail_response(400, 'DoesNotExist')
        obj.collection_count += 1
        obj.save()
        col = model()
        setattr(col, collection_type, obj)
        col.owner = Account.find_account_by_user(request.user)
        try:
            col.save()
        except IntegrityError:
            return self.fail_response(400, 'HasAlreadyAdded')
        return self.success_response(serializer(col).data)


class CollectionDetail(AuthView):
    def get(self, request, collection_type, format=None):
        lastid = request.GET.get('lastid', None)
        if collection_type == 'theme':
            model = ThemeCollection
            serializer = ThemeCollectionSerializer
        elif collection_type == 'series':
            model = SeriesCollection
            serializer = SeriesCollectionSerializer
        elif collection_type == 'recipe':
            model = RecipeCollection
            serializer = RecipeCollectionSerializer
        else:
            return self.fail_response(400, 'BadArgument')
        owner = Account.find_account_by_user(request.user)
        if lastid:
            result = model.objects.filter(owner=owner, id__lt=lastid).order_by('-created_time')[0:20]
        else:
            result = model.objects.filter(owner=owner).order_by('-created_time')[0:20]
        return self.success_response(serializer(result, many=True).data)
