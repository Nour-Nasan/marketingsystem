from django.db import models
from django.conf import settings
from products.models import Product

class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"Comment by {self.user.username}"
