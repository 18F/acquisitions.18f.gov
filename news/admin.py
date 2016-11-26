from django.contrib import admin
from news.models import Post


# Register your models here.
@admin.register(Post)
class NewsAdmin(admin.ModelAdmin):
    pass
