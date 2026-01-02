from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # ----- Seller URLs -----
    path('view/', views.view_orders, name='view_orders'),
    path('approve/<int:order_id>/', views.approve_order, name='approve_order'),
    path('reject/<int:order_id>/', views.reject_order, name='reject_order'),
    path('details/<int:order_id>/', views.order_details, name='order_details'),
    path('tracking/update/<int:order_id>/', views.update_order_tracking, name='update_order_tracking'),

    # ----- Buyer URLs -----
    path('create/', views.create_order, name='create_order'),
    path('create/', views.create_order, name='confirm_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('tracking/<int:order_id>/', views.order_tracking,name='order_tracking'),

]
