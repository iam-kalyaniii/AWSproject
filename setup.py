"""
College Event Portal – One-time setup script.
Run this ONCE after installing Django:

    python setup.py

It will:
  1. Apply all migrations
  2. Create admin superuser  (admin / admin123)
  3. Seed 3 sample halls
  4. Print instructions to run the server
"""

import os
import sys
import django

# Make sure we can import the project
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_event_portal.settings')

print("=" * 55)
print("  College Event Portal – Setup Script")
print("  ZIBACAR, Narhe, Pune")
print("=" * 55)

# ── Step 1: migrations ────────────────────────────────────
print("\n[1/3] Running database migrations...")
from django.core.management import call_command
django.setup()
call_command('migrate', verbosity=0)
print("      ✅ Migrations applied successfully.")

# ── Step 2: superuser ─────────────────────────────────────
print("\n[2/3] Creating admin superuser...")
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@zibacar.edu.in',
        password='admin123',
        first_name='Admin',
        last_name='ZIBACAR',
    )
    from halls.models import UserProfile
    UserProfile.objects.create(user=admin, user_type='faculty')
    print("      ✅ Superuser created → username: admin | password: admin123")
else:
    print("      ℹ️  Admin user already exists, skipping.")

# ── Step 3: seed halls ────────────────────────────────────
print("\n[3/3] Seeding sample halls...")
from halls.models import Hall

halls_data = [
    {
        "name": "Main Auditorium",
        "capacity": 500,
        "location": "Main Building, Ground Floor",
        "facilities": "Projector, AC, Sound System, Stage, Backstage Room, Wi-Fi",
    },
    {
        "name": "Conference Hall A",
        "capacity": 100,
        "location": "Admin Block, 2nd Floor",
        "facilities": "Projector, Whiteboard, AC, Video Conferencing",
    },
    {
        "name": "Seminar Hall",
        "capacity": 150,
        "location": "Academic Block, 1st Floor",
        "facilities": "Projector, AC, Podium, Wi-Fi",
    },
]

created = 0
for data in halls_data:
    hall, was_created = Hall.objects.get_or_create(name=data["name"], defaults=data)
    if was_created:
        created += 1

print(f"      ✅ {created} hall(s) seeded ({3 - created} already existed).")

# ── Done ──────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  ✅ Setup complete!")
print("=" * 55)
print("\n  Start the development server with:")
print("    python manage.py runserver")
print("\n  Then open:  http://127.0.0.1:8000/")
print("  Admin panel: http://127.0.0.1:8000/admin/")
print("  Custom dashboard: http://127.0.0.1:8000/dashboard/")
print("\n  Admin login: admin / admin123")
print("=" * 55)
