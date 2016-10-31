from django.contrib import admin
from team.models import Teammate, Role
from projects.models import IAA, Project


# Register your models here.
@admin.register(Teammate, Role)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(IAA, Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
