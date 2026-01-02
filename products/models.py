from django.db import models
from categories.models import Category 
from shops.models import Shop
from django.db.models import Avg

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    productPrice = models.DecimalField(max_digits=8, decimal_places=2)
    productImage = models.ImageField(upload_to='product_images/')
    productDescription = models.TextField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')


    def __str__(self):
        return self.productName
