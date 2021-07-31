from django.contrib import admin
from gadgetgateway.models import Category, Product , UserProfile

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(Product, ProductAdmin)

# admin.site.register(Comments)