from django.contrib import admin
from .models import Category, Product, ProductImage, Color, Size, ProductVariant


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_title', 'category_description', 'slug')
    search_fields = ('category_title',)
    prepopulated_fields = {"slug": ("category_title",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'product_category', 'product_price', 'sku', 'slug')
    list_filter = ('product_category',)
    search_fields = ('product_title', 'product_category__category_title', 'sku')
    prepopulated_fields = {"slug": ("product_title",)}
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',  'created_at')
    # list_filter = ('created_at')
    search_fields = ('product__product_title', 'alt_text')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color_name', 'size_name', 'varient_price', 'stock')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__product_title', 'color__name', 'size__name')
    
    def color_name(self, obj):
        return obj.color.name
    color_name.admin_order_field = 'color'  # Allows column order sorting
    color_name.short_description = 'Color'  # Renames column head

    def size_name(self, obj):
        return obj.color.name
    size_name.admin_order_field = 'size'  # Allows column order sorting
    size_name.short_description = 'size'  # Renames column head
