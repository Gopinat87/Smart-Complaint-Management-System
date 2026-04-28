from django.core.management.base import BaseCommand
from complaint_app.models import Category


CATEGORIES = [
    ('Water Supply',      '💧'),
    ('Electricity',       '⚡'),
    ('Sanitation',        '🗑️'),
    ('Roads & Pathways',  '🛣️'),
    ('Security',          '🔒'),
    ('Internet / Wi-Fi',  '📶'),
    ('Noise Complaint',   '🔊'),
    ('Maintenance',       '🔧'),
    ('Pest Control',      '🐛'),
    ('Other',             '📋'),
]


class Command(BaseCommand):
    help = 'Seed default complaint categories'

    def handle(self, *args, **kwargs):
        for name, icon in CATEGORIES:
            obj, created = Category.objects.get_or_create(name=name, defaults={'icon': icon})
            status = 'Created' if created else 'Exists '
            self.stdout.write(f'  {status}: {icon}  {name}')
        self.stdout.write(self.style.SUCCESS('✅ Categories seeded.'))
