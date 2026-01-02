from django.db import models
from django.contrib.auth import get_user_model
from shops.models import Shop

User = get_user_model()

class Conversation(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_conversations')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_conversations')
    related_shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    deleted_by_buyer = models.BooleanField(default=False)
    deleted_by_seller = models.BooleanField(default=False)
    class Meta:
        unique_together = ('buyer', 'seller', 'related_shop')
        ordering = ['-last_updated']

    def __str__(self):
        return f"Chat between {self.buyer.username} and {self.seller.username} (Shop: {self.related_shop.shopName})"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender.username} at {self.timestamp}"
