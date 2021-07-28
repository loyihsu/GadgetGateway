from django.contrib import admin
from django.db.models.query_utils import PathInfo
from rango.models import Category, Page

admin.site.register(Category)
admin.site.register(Page)