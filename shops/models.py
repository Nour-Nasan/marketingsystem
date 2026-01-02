from django.db import models
from users.models import CustomUser


class Shop(models.Model):
    id = models.AutoField(primary_key=True)  
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='shop')
    shopName = models.CharField(max_length=100, unique=True)
    shopDescription = models.TextField(max_length=1000)
    shopAddress = models.CharField(max_length=300)
    shopNumber = models.CharField(max_length=20)
    shopEmail = models.EmailField(blank=True,null=True)

    
    def __str__(self):
        return self.shopName


