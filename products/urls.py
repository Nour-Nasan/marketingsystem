from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # -------- Seller Product Management --------
    path('manage/', views.manage_products, name='manage_products'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # -------- Buyer Browse Products (Unified Page) --------
    path('browse/', views.search_by_category, name='search_by_category'),

    # -------- Backward Compatibility (optional but safe) --------
    path('all/', views.search_by_category),
    path('list/', views.search_by_category),
    path('filter/', views.search_by_category),

    # -------- Product Details --------
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]

