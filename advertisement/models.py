from django.db import models
from django.conf import settings

class Advertisement(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )

    image = models.ImageField(upload_to='advertisements/')

    def __str__(self):
        return f"Advertisement {self.id}"
