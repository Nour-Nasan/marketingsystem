from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    # Buyer
    path('', views.shop_list, name='shop_list'),
    path('<int:shop_id>/', views.shop_detail, name='shop_detail'),

    # Seller
    path('my-shop/', views.manage_shop, name='manage_shop'),
    path('add/', views.add_shop, name='add_shop'),
    path('edit/', views.edit_shop, name='edit_shop'),
    path('delete/<int:shop_id>/', views.delete_shop, name='delete_shop'),
]
