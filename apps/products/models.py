from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from apps.base.models import BaseModel

class Category(BaseModel):
    category_title = models.CharField(max_length=100)
    category_description = models.TextField(blank=True)
    slug = models.SlugField(unique=True , null=True , blank=True, editable=True)
    category_image = models.ImageField(upload_to="catgories")

    def __str__(self):
        return self.category_title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories" # what name to be shown on admin site


    
class Product(BaseModel):
    sku_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]*$',
        message='SKU must contain only letters, numbers, hyphens, and underscores.'
    )

    product_title = models.CharField(max_length=256)
    product_description = models.TextField(null= True, blank=True)
    product_category = models.ForeignKey(Category,on_delete= models.CASCADE, related_name= "products")
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True) 
    slug = models.SlugField(unique=True, null=True, blank=True)


    def __str__(self):
        return self.product_title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_title)
        super(Product, self).save(*args, **kwargs)




# LEARN : https://stackoverflow.com/questions/61647633/how-to-show-variations-sizes-of-products-in-django-admin



class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.product.product_title}"
    

#VARIATION MODEL:
class Color(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name
    

class Size(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name
    

class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    varient_sku = models.CharField(max_length=100, unique=True, validators=[Product.sku_validator])
    varient_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    
    def str(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"

'''
class ProductAttribute(models.Model):
    name = models.CharField(max_length=50, unique=True)
    products = models.ManyToManyField(Product, related_name='attributes')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Variation Type"
        verbose_name_plural = "Variation Types" # waht name to be shown on admin site

class AttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    class Meta:
        unique_together = ('attribute', 'value')

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    
    class Meta:
        verbose_name = "Varient Name"
        verbose_name_plural = "Variations" # waht name to be shown on admin site

class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    attribute_values = models.ManyToManyField(AttributeValue, related_name='variants')
    sku = models.CharField(max_length=100, unique=True, validators=[Product.sku_validator])
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.product_title} - {', '.join(str(av) for av in self.attribute_values.all())}"

    def save(self, *args, **kwargs):
        if not self.sku:
            base_sku = self.product.sku
            variant_part = '-'.join(str(av.value) for av in self.attribute_values.all())
            self.sku = f"{base_sku}-{variant_part}"
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.product.base_price + self.price_adjustment

    def clean(self):
        super().clean()
        if self.price_adjustment and self.final_price < 0:
            raise ValidationError("Final price cannot be negative.")

class VariantImage(BaseModel):
    variant = models.ForeignKey(ProductVariant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="variant_images")
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.variant}"

class SizeVariant(models.Model):
    sku_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]*$',
        message='SKU must contain only letters, numbers, hyphens, and underscores.'
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='size_variants')
    size_name = models.CharField(max_length=50)
    sku = models.CharField(max_length=100, unique=True)
    varient_price = models.DecimalField(max_digits=10, decimal_places=2)  
    def __str__(self):
        return self.size_name
    
class ProductImages(BaseModel):
    product = models.ForeignKey('Product', related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images",)

'''