from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from apps.base.models import BaseModel
from django.utils.text import slugify

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
        verbose_name_plural = "Categories" # waht name to be shown on admin site


    


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


# class Coupon(BaseModel):
#     DISCOUNT_TYPE_CHOICES = (
#         ('percentage', 'Percentage'),
#         ('fixed', 'Fixed Amount'),
#     )

#     code = models.CharField(max_length=50, unique=True)
#     valid_from = models.DateTimeField()
#     valid_to = models.DateTimeField()
#     discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
#     discount = models.DecimalField(
#         max_digits=5, 
#         decimal_places=2, 
#         validators=[MinValueValidator(0), MaxValueValidator(100)]
#     )
#     active = models.BooleanField()
#     customer_segments = models.ManyToManyField(CustomerSegment, blank=True)

#     def __str__(self):
#         return self.code