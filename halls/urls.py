from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.index, name='index'),
    path('book/<int:hall_id>/', views.book_hall, name='book_hall'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # Admin (custom)
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('dashboard/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('dashboard/booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('dashboard/halls/', views.manage_halls, name='manage_halls'),
    path('dashboard/halls/add/', views.add_hall, name='add_hall'),
    path('dashboard/halls/edit/<int:hall_id>/', views.edit_hall, name='edit_hall'),
    path('dashboard/halls/delete/<int:hall_id>/', views.delete_hall, name='delete_hall'),
]
