from django.contrib import admin
from team.models import Teammate, Role


# Register your models here.
@admin.register(Teammate, Role)
class TeamAdmin(admin.ModelAdmin):
    pass
