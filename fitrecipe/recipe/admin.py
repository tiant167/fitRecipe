#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: chaihaotian
# @Date:   2015-04-26 14:30:44
# @Last Modified by:   chaihaotian
# @Last Modified time: 2015-07-14 20:27:43
from django.contrib import admin

from .models import Recipe, Ingredient
# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'calories', 'duration')
    list_display_links = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('labels',)
    list_filter = ('labels',)
    readonly_fields = ('macro_element_ratio', 'protein_ratio', 'fat_ratio')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
