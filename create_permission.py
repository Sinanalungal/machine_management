import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axis_tracking.settings')
django.setup()

from django.contrib.auth.models import Group, Permission

def start_data_generation():

    Group.objects.get_or_create(name='SUPERADMIN')
    Group.objects.get_or_create(name='Manager')
    Group.objects.get_or_create(name='Supervisor')
    Group.objects.get_or_create(name='Operator')


if __name__ == "__main__":
    print("creating permissions")
    start_data_generation()