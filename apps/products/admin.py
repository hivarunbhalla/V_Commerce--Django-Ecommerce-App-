from django.contrib import admin
from .models import (Category, 
                    Product,
                    ProductImages,
                    SizeVariant,
                    )

class CategoryAdmin(admin.ModelAdmin):
    model = Category

class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


class SizeVariantInline(admin.TabularInline):
    model = SizeVariant
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline, SizeVariantInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)