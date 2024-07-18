from django.contrib import admin
from .models import Category, Product, ProductImages

class CategoryAdmin(admin.ModelAdmin):
    model = Category

class ProductImagesInline(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)