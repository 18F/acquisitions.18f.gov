from django.contrib import admin
from projects.models import IAA, Project, Buy


# Register your models here.
@admin.register(IAA, Project, Buy)
class ProjectAdmin(admin.ModelAdmin):
    pass
