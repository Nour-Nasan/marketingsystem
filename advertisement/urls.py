from django.urls import path
from . import views

app_name = 'advertisement'

urlpatterns = [
    path('my/', views.my_ads, name='my_ads'),
    path('add/', views.add_advertisement, name='add_ad'),
    path('edit/<int:ad_id>/', views.edit_advertisement, name='edit_ad'),
    path('delete/<int:ad_id>/', views.delete_advertisement, name='delete_ad'),
    path('show/', views.show_advertisements, name='show_ads'),
]
