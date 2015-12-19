from django.contrib import admin

# Register your models here.
from .models import PlanAuthor, Plan


class PlanAdmin(admin.ModelAdmin):
    list_filter = ('is_personal',)

admin.site.register(PlanAuthor)
admin.site.register(Plan, PlanAdmin)
