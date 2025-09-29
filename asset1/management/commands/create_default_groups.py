from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from asset1.models import Asset

class Command(BaseCommand):
    help = "Create Admin, Manager, Employee groups"

    def handle(self, *args, **options):
        Group.objects.get_or_create(name="Admin")
        Group.objects.get_or_create(name="Manager")
        Group.objects.get_or_create(name="Employee")
        self.stdout.write(self.style.SUCCESS("Groups ensured."))
