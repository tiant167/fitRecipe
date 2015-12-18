#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from rest_framework import serializers
from base.serializers import BaseSerializer
from recipe.models import Recipe, Ingredient
from .models import PlanAuthor, Plan, Calendar, Punch
from recipe.serializers import RecipeSerializer, IngredientSerializer



class PlanAuthorSerializer(BaseSerializer):
    class Meta:
        model = PlanAuthor


class PlanSerializer(BaseSerializer):
    author = PlanAuthorSerializer()

    class Meta:
        model = Plan

    def to_representation(self, obj):
        '''
        加上简单模式，用于列表展示
        '''
        r = super(PlanSerializer, self).to_representation(obj)
        simple = self.context.get('simple', True)
        if simple:
            # 去掉 component_set, procedure_set, nutrition_set
            pop_keys = ('routines',)
            for k in pop_keys:
                r.pop(k, None)
        else:
            r['routines'] = json.loads(r['routines'] or '[]')
            # populate recipe & ingredient
            # TODO: 这里可以做 prefect
            for item in r['routines']:
                for d in item['dish']:
                    for recipe in d['recipe']:
                        try:
                            recipe['content'] = RecipeSerializer(Recipe.objects.get(pk=recipe['id'])).data
                        except Recipe.DoesNotExist:
                            recipe['content'] = None
                    for ingredient in d['ingredient']:
                        try:
                            ingredient['content'] = IngredientSerializer(Ingredient.objects.get(pk=ingredient['id'])).data
                        except Ingredient.DoesNotExist:
                            ingredient['content'] = None
        return r


class CalendarSerializer(BaseSerializer):
    plan = PlanSerializer()

    class Meta:
        model = Calendar


class PunchSerializer(BaseSerializer):
    class Meta:
        model = Punch
