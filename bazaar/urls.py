from django.urls import path

from . import views

app_name = 'bazaar'

urlpatterns = [
    path('my-bazaars/', views.my_bazaars, name='my_bazaars'),
    path('add/', views.add_bazaar, name='add_bazaar'),
    path('edit/<int:bazaar_id>/', views.edit_bazaar, name='edit_bazaar'),
    path('delete/<int:bazaar_id>/', views.delete_bazaar, name='delete_bazaar'),
]
