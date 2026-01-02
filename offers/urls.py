from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('add/', views.add_offer, name='add_offer'),
    path('my/', views.my_offers, name='my_offers'),
    path('edit/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('delete/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('show/', views.show_offers, name='show_offers'),
]
