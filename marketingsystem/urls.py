from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # صفحة المسؤول
    path('admin/', admin.site.urls),

    path("", include('users.urls')),

    # مسارات التطبيقات
    path('users/', include('users.urls')),
    path('shops/', include('shops.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('baskets/', include('baskets.urls')),
    path('comments/', include('comments.urls')),
    path('categories/', include('categories.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('advertisement/', include('advertisement.urls')),
    path('offers/', include('offers.urls')),
    path('reports/', include('reports.urls')),
    path('chat/', include('chat.urls')),
    path('recommendations/', include('recommendations.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
