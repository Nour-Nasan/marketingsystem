from django.contrib import admin

from .models import Bazaar, BazaarBooking


@admin.register(Bazaar)
class BazaarAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'organizer',
        'location',
        'start_datetime',
        'end_datetime',
        'table_price',
        'created_at',
    )
    list_filter = ('start_datetime', 'end_datetime', 'created_at')
    search_fields = ('title', 'location', 'description')
    ordering = ('-start_datetime',)


@admin.register(BazaarBooking)
class BazaarBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'bazaar', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('seller__username', 'bazaar__title')
    ordering = ('-created_at',)
