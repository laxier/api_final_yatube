from django.contrib import admin
from posts.models import Group

# Регистрируем модель групп
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    search_fields = ('title',)
