from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime
from .models import Hall, Booking, UserProfile


# ─────────────────────────────────────────────
# HOME – list all available halls
# ─────────────────────────────────────────────
def index(request):
    halls = Hall.objects.filter(is_available=True)
    return render(request, 'halls/index.html', {'halls': halls})


# ─────────────────────────────────────────────
# BOOK A HALL
# ─────────────────────────────────────────────
def book_hall(request, hall_id):
    hall = get_object_or_404(Hall, id=hall_id, is_available=True)

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        user_email = request.POST.get('user_email', '').strip()
        user_type = request.POST.get('user_type', '').strip()
        event_name = request.POST.get('event_name', '').strip()
        event_description = request.POST.get('event_description', '').strip()
        booking_date = request.POST.get('booking_date', '').strip()
        start_time = request.POST.get('start_time', '').strip()
        end_time = request.POST.get('end_time', '').strip()

        # Basic validation
        if not all([user_name, user_email, user_type, event_name,
                    event_description, booking_date, start_time, end_time]):
            messages.error(request, 'All fields are required.')
            return render(request, 'halls/book_hall.html', {'hall': hall})

        try:
            b_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return render(request, 'halls/book_hall.html', {'hall': hall})

        if b_date < date.today():
            messages.error(request, 'Booking date cannot be in the past.')
            return render(request, 'halls/book_hall.html', {'hall': hall})

        if start_time >= end_time:
            messages.error(request, 'End time must be after start time.')
            return render(request, 'halls/book_hall.html', {'hall': hall})

        # Conflict check
        conflicts = Booking.objects.filter(
            hall=hall,
            booking_date=b_date,
            status__in=['pending', 'approved']
        ).filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if conflicts.exists():
            messages.error(request, 'This hall is already booked for the selected time slot. Please choose a different time.')
            return render(request, 'halls/book_hall.html', {'hall': hall})

        booking = Booking(
            hall=hall,
            user=request.user if request.user.is_authenticated else None,
            user_name=user_name,
            user_email=user_email,
            user_type=user_type,
            event_name=event_name,
            event_description=event_description,
            booking_date=b_date,
            start_time=start_time,
            end_time=end_time,
        )
        booking.save()
        messages.success(request, f'Booking submitted successfully for "{event_name}"! Awaiting admin approval.')
        return redirect('my_bookings')

    # Pre-fill form for logged-in users
    initial = {}
    if request.user.is_authenticated:
        initial['user_name'] = request.user.get_full_name() or request.user.username
        initial['user_email'] = request.user.email
        if hasattr(request.user, 'profile'):
            initial['user_type'] = request.user.profile.user_type

    return render(request, 'halls/book_hall.html', {'hall': hall, 'initial': initial})


# ─────────────────────────────────────────────
# MY BOOKINGS – email-based lookup
# ─────────────────────────────────────────────
def my_bookings(request):
    email = request.GET.get('email', '').strip()
    bookings = []

    if request.user.is_authenticated and not email:
        email = request.user.email

    if email:
        bookings = Booking.objects.filter(user_email__iexact=email).select_related('hall')

    return render(request, 'halls/my_bookings.html', {'bookings': bookings, 'email': email})


# ─────────────────────────────────────────────
# CANCEL BOOKING
# ─────────────────────────────────────────────
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    email = booking.user_email

    # Only pending bookings can be cancelled
    if booking.status != 'pending':
        messages.error(request, 'Only pending bookings can be cancelled.')
        return redirect(f'/my-bookings/?email={email}')

    booking.delete()
    messages.success(request, 'Booking cancelled successfully.')
    return redirect(f'/my-bookings/?email={email}')


# ─────────────────────────────────────────────
# AUTH – Register
# ─────────────────────────────────────────────
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        user_type = request.POST.get('user_type', 'student')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([username, email, full_name, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'halls/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'halls/register.html')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'halls/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'halls/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'halls/register.html')

        # Split full name
        parts = full_name.split(' ', 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first,
            last_name=last,
        )
        UserProfile.objects.create(user=user, user_type=user_type)
        login(request, user)
        messages.success(request, f'Welcome, {first}! Account created successfully.')
        return redirect('index')

    return render(request, 'halls/register.html')


# ─────────────────────────────────────────────
# AUTH – Login
# ─────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'halls/login.html')


# ─────────────────────────────────────────────
# AUTH – Logout
# ─────────────────────────────────────────────
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


# ─────────────────────────────────────────────
# ADMIN DASHBOARD (custom — not Django admin)
# ─────────────────────────────────────────────
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('index')

    # Filters
    status_filter = request.GET.get('status', '')
    user_type_filter = request.GET.get('user_type', '')
    date_filter = request.GET.get('date_range', '')
    hall_filter = request.GET.get('hall', '')
    search = request.GET.get('search', '').strip()

    bookings = Booking.objects.select_related('hall', 'user').all()

    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if user_type_filter:
        bookings = bookings.filter(user_type=user_type_filter)
    if hall_filter:
        bookings = bookings.filter(hall_id=hall_filter)
    if search:
        bookings = bookings.filter(
            Q(event_name__icontains=search) |
            Q(user_name__icontains=search) |
            Q(user_email__icontains=search)
        )

    today = date.today()
    if date_filter == 'today':
        bookings = bookings.filter(booking_date=today)
    elif date_filter == 'week':
        from datetime import timedelta
        bookings = bookings.filter(booking_date__gte=today - timedelta(days=7))
    elif date_filter == 'month':
        bookings = bookings.filter(booking_date__month=today.month, booking_date__year=today.year)

    # Stats
    total = Booking.objects.count()
    pending = Booking.objects.filter(status='pending').count()
    approved = Booking.objects.filter(status='approved').count()
    rejected = Booking.objects.filter(status='rejected').count()

    halls = Hall.objects.all()

    context = {
        'bookings': bookings,
        'halls': halls,
        'total': total,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'status_filter': status_filter,
        'user_type_filter': user_type_filter,
        'date_filter': date_filter,
        'hall_filter': hall_filter,
        'search': search,
    }
    return render(request, 'halls/admin_dashboard.html', context)


# ─────────────────────────────────────────────
# APPROVE / REJECT BOOKING
# ─────────────────────────────────────────────
def approve_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect('index')
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'approved'
    booking.admin_remarks = request.POST.get('remarks', '')
    booking.save()
    messages.success(request, f'Booking "{booking.event_name}" approved.')
    return redirect('admin_dashboard')


def reject_booking(request, booking_id):
    if not request.user.is_staff:
        return redirect('index')
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'rejected'
    booking.admin_remarks = request.POST.get('remarks', '')
    booking.save()
    messages.warning(request, f'Booking "{booking.event_name}" rejected.')
    return redirect('admin_dashboard')


# ─────────────────────────────────────────────
# MANAGE HALLS (Admin)
# ─────────────────────────────────────────────
def manage_halls(request):
    if not request.user.is_staff:
        return redirect('index')
    halls = Hall.objects.all()
    return render(request, 'halls/manage_halls.html', {'halls': halls})


def add_hall(request):
    if not request.user.is_staff:
        return redirect('index')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        capacity = request.POST.get('capacity', 0)
        location = request.POST.get('location', '').strip()
        facilities = request.POST.get('facilities', '').strip()

        if not all([name, capacity, location, facilities]):
            messages.error(request, 'All fields are required.')
            return render(request, 'halls/add_hall.html')

        Hall.objects.create(name=name, capacity=int(capacity), location=location, facilities=facilities)
        messages.success(request, f'Hall "{name}" added successfully.')
        return redirect('manage_halls')

    return render(request, 'halls/add_hall.html')


def edit_hall(request, hall_id):
    if not request.user.is_staff:
        return redirect('index')
    hall = get_object_or_404(Hall, id=hall_id)

    if request.method == 'POST':
        hall.name = request.POST.get('name', hall.name).strip()
        hall.capacity = int(request.POST.get('capacity', hall.capacity))
        hall.location = request.POST.get('location', hall.location).strip()
        hall.facilities = request.POST.get('facilities', hall.facilities).strip()
        hall.is_available = request.POST.get('is_available') == 'on'
        hall.save()
        messages.success(request, f'Hall "{hall.name}" updated successfully.')
        return redirect('manage_halls')

    return render(request, 'halls/edit_hall.html', {'hall': hall})


def delete_hall(request, hall_id):
    if not request.user.is_staff:
        return redirect('index')
    hall = get_object_or_404(Hall, id=hall_id)
    name = hall.name
    hall.delete()
    messages.success(request, f'Hall "{name}" deleted.')
    return redirect('manage_halls')


# ─────────────────────────────────────────────
# BOOKING DETAIL
# ─────────────────────────────────────────────
def booking_detail(request, booking_id):
    if not request.user.is_staff:
        return redirect('index')
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'halls/booking_detail.html', {'booking': booking})
