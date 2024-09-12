# Generated by Django 4.0 on 2024-09-11 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Axis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('axis_name', models.CharField(choices=[('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('A', 'A'), ('C', 'C')], max_length=1)),
                ('max_acceleration', models.FloatField()),
                ('max_velocity', models.FloatField()),
                ('actual_position', models.FloatField()),
                ('target_position', models.FloatField()),
                ('homed', models.BooleanField()),
                ('acceleration', models.FloatField()),
                ('velocity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FieldData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_position', models.FloatField()),
                ('target_position', models.FloatField()),
                ('distance_to_go', models.FloatField()),
                ('acceleration', models.FloatField()),
                ('velocity', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_id', models.CharField(max_length=50, unique=True)),
                ('machine_name', models.CharField(max_length=100, unique=True)),
                ('tool_capacity', models.IntegerField()),
                ('tool_offset', models.FloatField()),
                ('feedrate', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ToolsInUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_in_use', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('machine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mechine_manage_app.machine')),
            ],
        ),
        migrations.AddIndex(
            model_name='machine',
            index=models.Index(fields=['machine_id'], name='mechine_man_machine_f48b2d_idx'),
        ),
        migrations.AddIndex(
            model_name='machine',
            index=models.Index(fields=['machine_name'], name='mechine_man_machine_0a4275_idx'),
        ),
        migrations.AddField(
            model_name='fielddata',
            name='axis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mechine_manage_app.axis'),
        ),
        migrations.AddField(
            model_name='axis',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mechine_manage_app.machine'),
        ),
        migrations.AddIndex(
            model_name='toolsinuse',
            index=models.Index(fields=['machine'], name='mechine_man_machine_ba8ac5_idx'),
        ),
        migrations.AddIndex(
            model_name='fielddata',
            index=models.Index(fields=['axis'], name='mechine_man_axis_id_44792c_idx'),
        ),
        migrations.AddIndex(
            model_name='axis',
            index=models.Index(fields=['machine'], name='mechine_man_machine_30d65c_idx'),
        ),
        migrations.AddIndex(
            model_name='axis',
            index=models.Index(fields=['axis_name'], name='mechine_man_axis_na_395f8d_idx'),
        ),
    ]
