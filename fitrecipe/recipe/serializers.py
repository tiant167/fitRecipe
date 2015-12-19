#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: chaihaotian
# @Date:   2015-04-26 15:52:14
# @Last Modified by:   chaihaotian
# @Last Modified time: 2015-07-14 20:27:49
import json

from rest_framework import serializers
from .models import Recipe, Ingredient
from accounts.serializers import OtherAuthorSerializer
from base.serializers import BaseSerializer
from label.serializers import LabelSerializer
from comment.serializers import CommentSerializer

class IngredientSerializer(BaseSerializer):

    class Meta:
        model = Ingredient


class RecipeSerializer(BaseSerializer):
    labels = LabelSerializer(many=True, read_only=True)
    macro_element_ratio = serializers.CharField()
    protein_ratio = serializers.CharField()
    fat_ratio = serializers.CharField()
    author = OtherAuthorSerializer(value=('id', 'nick_name', 'avatar'), read_only=True)

    class Meta:
        model = Recipe

    def to_representation(self, obj):
        '''
        加上简单模式，用于列表展示
        '''
        r = super(RecipeSerializer, self).to_representation(obj)
        simple = self.context.get('simple', True)
        if simple:
            # 去掉 component_set, procedure_set, nutrition_set
            pop_keys = ('procedures', 'components', 'water', 'energy', 'protein',
                'fat', 'carbohydrate', 'sodium', 'vc', 'vd', 'fatty_acids',
                'cholesterol', 'fiber')
            for k in pop_keys:
                r.pop(k, None)
        else:
            r['procedures'] = json.loads(r['procedures'] or '[]')
            r['components'] = json.loads(r['components'] or '[]')
        return r
