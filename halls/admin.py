from django.contrib import admin
from .models import Hall, Booking, UserProfile


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'location', 'is_available', 'created_at']
    list_filter = ['is_available']
    search_fields = ['name', 'location']
    list_editable = ['is_available']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'hall', 'user_name', 'user_type', 'booking_date', 'start_time', 'end_time', 'status', 'created_at']
    list_filter = ['status', 'user_type', 'booking_date', 'hall']
    search_fields = ['event_name', 'user_name', 'user_email']
    list_editable = ['status']
    date_hierarchy = 'booking_date'

    actions = ['approve_bookings', 'reject_bookings']

    def approve_bookings(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'{queryset.count()} booking(s) approved.')
    approve_bookings.short_description = 'Approve selected bookings'

    def reject_bookings(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} booking(s) rejected.')
    reject_bookings.short_description = 'Reject selected bookings'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone']
    list_filter = ['user_type']
    search_fields = ['user__username', 'user__email']
