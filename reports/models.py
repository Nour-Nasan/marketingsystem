from django.db import models
from shops.models import Shop

class ShopVisit(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='shop_visits'  
    )
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit to {self.shop.shopName}"
