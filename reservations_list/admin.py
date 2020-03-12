from django.contrib import admin

from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'arrival', 'departure',  'name', 'status')
    list_display_links = ('id', 'number')
    list_filter = ['arrival', 'departure', 'status']
    search_fields = ('number', 'arrival', 'departure', 'status', 'name', 'no_of_people')
    list_per_page = 25


admin.site.register(Reservation, ReservationAdmin)
