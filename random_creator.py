import random
import time
from datetime import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'axis_tracking.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from mechine_manage_app.models import Machine, Axis, FieldData, ToolsInUse


NUM_MACHINES = 20
AXES = ['X', 'Y', 'Z', 'A', 'C']

TOOL_OFFSET_UPDATE_INTERVAL = 15 * 60
FEEDRATE_UPDATE_INTERVAL = 15 * 60
TOOL_IN_USE_UPDATE_INTERVAL = 5 * 60
AXIS_UPDATE_INTERVAL = 0.1


def create_or_update_machines():
    for i in range(NUM_MACHINES):
        machine_id = 81258856 + i
        machine_name = f'EMXP{i + 1}'

        machine, created = Machine.objects.update_or_create(
            machine_id=machine_id,
            defaults={
                'machine_name': machine_name,
                'tool_capacity': 24,
                'tool_offset': random.uniform(5, 40),
                'feedrate': random.randint(0, 20000),
            }
        )

        generate_tools_in_use(machine)
        generate_axis_data(machine)


def generate_tools_in_use(machine):
    ToolsInUse.objects.update_or_create(
        machine=machine,
        defaults={
            'tool_in_use': random.randint(1, 24),
        }
    )


def generate_axis_data(machine):
    for axis_name in AXES:
        Axis.objects.update_or_create(
            machine=machine,
            axis_name=axis_name,
            defaults={
                'max_acceleration': 200,
                'max_velocity': 60,
                'actual_position': random.uniform(-190, 190),
                'target_position': random.uniform(-190, 191),
                'homed': random.choice([0, 1]),
                'acceleration': random.uniform(0, 150),
                'velocity': random.uniform(0, 80)
            }
        )

# Update dynamic fields for the machine


def update_machine_data(machine):
    machine.tool_offset = random.uniform(5, 40)
    machine.feedrate = random.randint(0, 20000)
    ToolsInUse.objects.update_or_create(
        machine=machine,
        defaults={
            'tool_in_use': random.randint(1, machine.tool_capacity),
        }
    )
    machine.save()


def update_axis_data(machine):
    for axis in Axis.objects.filter(machine=machine):
        axis.actual_position = random.uniform(-190, 190)
        axis.target_position = random.uniform(-190, 191)
        axis.acceleration = random.uniform(0, 150)
        axis.velocity = random.uniform(0, 80)
        axis.homed = random.choice([0, 1])
        axis.save()

        FieldData.objects.create(
            axis=axis,
            actual_position=axis.actual_position,
            target_position=axis.target_position,
            distance_to_go=axis.target_position - axis.actual_position,
            acceleration=axis.acceleration,
            velocity=axis.velocity
        )


def start_data_generation():
    last_tool_offset_update = time.time()
    last_tool_in_use_update = time.time()

    Group.objects.get_or_create(name='SUPERADMIN')
    Group.objects.get_or_create(name='Manager')
    Group.objects.get_or_create(name='Supervisor')
    Group.objects.get_or_create(name='Operator')

    try:
        create_or_update_machines()

        while True:
            current_time = time.time()

            for machine in Machine.objects.all():
                if current_time - last_tool_offset_update >= TOOL_OFFSET_UPDATE_INTERVAL:
                    update_machine_data(machine)
                    last_tool_offset_update = current_time

                if current_time - last_tool_in_use_update >= TOOL_IN_USE_UPDATE_INTERVAL:

                    ToolsInUse.objects.update_or_create(
                        machine=machine,
                        defaults={
                            'tool_in_use': random.randint(1, machine.tool_capacity),
                        }
                    )
                    last_tool_in_use_update = current_time

                update_axis_data(machine)

            time.sleep(AXIS_UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("Data generation stopped.")


if __name__ == "__main__":
    print("Starting data generation for 20 machines with 5 axes each...")
    start_data_generation()
