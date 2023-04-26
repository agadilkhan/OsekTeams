from django.contrib import admin
from api.models import *

# Register your models here.
@admin.register(Category)
class CategorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')