from django.contrib import admin
import nested_admin

# Register your models here.
from .models import PlanAuthor, Plan, Dish, Routine, SingleIngredient, SingleRecipe


class SingleIngredientInline(nested_admin.NestedStackedInline):
    model = SingleIngredient


class SingleRecipeInline(nested_admin.NestedStackedInline):
    model = SingleRecipe


class DishInline(nested_admin.NestedStackedInline):
    model = Dish
    inlines = (SingleIngredientInline, SingleRecipeInline)


class RoutineAdmin(nested_admin.NestedAdmin):
    model = Routine
    inlines = (DishInline, )
    list_filter = ('plan__is_personal',)


class PlanAdmin(admin.ModelAdmin):
    list_filter = ('is_personal',)

admin.site.register(PlanAuthor)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Routine, RoutineAdmin)
