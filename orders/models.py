from django.db import models
from django.conf import settings
from baskets.models import Basket
from products.models import Product


CONTACT_METHOD_CHOICES = [
    ('phone', 'Phone'),
    ('email', 'Email'),
]

DELIVERY_METHOD_CHOICES = [
    ('internal', 'Internal'),
    ('manual', 'Manual'),
    ('shipping', 'Shipping'),
]


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('delivered', 'Delivered'),
        ('rejected', 'Rejected'),
    ]

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Basket"
    )

    contact_method = models.CharField(
        max_length=10,
        choices=CONTACT_METHOD_CHOICES,
        default='phone',
        verbose_name="وسيلة التواصل"
    )

    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_METHOD_CHOICES,
        default='internal',
        verbose_name="طريقة التوصيل"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Order Status"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} for {self.buyer.username}"

    def approve(self):
        self.status = 'approved'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.productName} (طلب #{self.order.id})"


class OrderTracking(models.Model):
    TRACKING_STATUS_CHOICES = [
        ('preparing', 'Preparing'),
        ('prepared', 'Prepared'),
        ('shipping', 'Shipping'),
        ('delivered','Delivered' ),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='tracking_steps'
    )

    status = models.CharField(
        max_length=20,
        choices=TRACKING_STATUS_CHOICES
    )

    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order.id} - {self.get_status_display()}"
