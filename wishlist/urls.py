from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.view_wishlist, name='view_wishlist'),
    path('toggle/<int:product_id>/', views.toggle_wishlist, name='toggle'),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
]
