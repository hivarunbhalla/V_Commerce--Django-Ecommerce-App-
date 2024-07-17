from django.db import models
from ..base.models import BaseModel


class Category(BaseModel):
    category_title = models.CharField(max_length=100)
    category_description = models.TextField(blank=True)
    slug = models.SlugField(unique=True , null=True , blank=True)
    category_image = models.ImageField(upload_to="catgories")

    def __str__(self):
        return self.category_title
    

class Product(BaseModel):
    product_title = models.CharField(max_length=256)
    product_description = models.TextField
    product_category = models.ForeignKey(Category,on_delete= models.CASCADE, related_name= "products")
    product_price = models.IntegerField()
    slug = models.SlugField(unique=True, null=True, blank=True)


class ProductImages(BaseModel):
    product = models.ForeignKey('Product', related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images",)
