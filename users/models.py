from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', _('Admin')),       
        ('buyer', _('Buyer')),
        ('seller',_('Seller')),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='buyer',
        verbose_name=_('Role'),
        help_text=_('Defines the role of the user in the system.')
    )
    
    REQUIRED_FIELDS = ['email', 'role']  

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def is_buyer(self):
        return self.role == 'buyer'

    def is_seller(self):
        return self.role == 'seller'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"