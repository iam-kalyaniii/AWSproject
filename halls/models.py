from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


class Hall(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=200)
    facilities = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]

    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    event_name = models.CharField(max_length=200)
    event_description = models.TextField()
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event_name} | {self.hall.name} | {self.booking_date}"

    class Meta:
        ordering = ['-created_at']
