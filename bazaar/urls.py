from django.urls import path

from . import views

app_name = 'bazaar'

urlpatterns = [
    path('my-bazaars/', views.my_bazaars, name='my_bazaars'),
    path('add/', views.add_bazaar, name='add_bazaar'),
    path('edit/<int:bazaar_id>/', views.edit_bazaar, name='edit_bazaar'),
    path('delete/<int:bazaar_id>/', views.delete_bazaar, name='delete_bazaar'),
    path('browse/', views.browse_bazaars, name='browse_bazaars'),
    path('detail/<int:bazaar_id>/', views.bazaar_detail, name='bazaar_detail'),
    path('book/<int:bazaar_id>/', views.confirm_booking, name='confirm_booking'),
    path('book-legacy/<int:bazaar_id>/', views.request_booking, name='request_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('organizer/bookings/', views.organizer_bookings, name='organizer_bookings'),
    path(
        'booking/<int:booking_id>/approve/',
        views.update_booking_status,
        {'status': 'approved'},
        name='approve_booking',
    ),
    path(
        'booking/<int:booking_id>/reject/',
        views.update_booking_status,
        {'status': 'rejected'},
        name='reject_booking',
    ),
]
