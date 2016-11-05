from django.contrib import admin
from projects.models import IAA, Project


# Register your models here.
@admin.register(IAA, Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
