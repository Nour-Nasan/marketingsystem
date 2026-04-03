from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('error-403/', views.error_403, name='error_403'),
        # ------------------ Admin Views ------------------
    path('admin-dashboard/add-shop/', views.add_shop_admin, name='add_shop_admin'),
    path('admin-dashboard/delete-shop/<int:shop_id>/', views.delete_shop_admin, name='delete_shop_admin'),

]
