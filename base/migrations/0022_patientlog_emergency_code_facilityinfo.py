# Generated by Django 4.1.5 on 2023-07-06 12:44

import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_patientlog_test_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientlog',
            name='emergency_code',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='FacilityInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recId', models.CharField(max_length=10, unique=True)),
                ('facility_name', models.CharField(default='Hospillar M.S', max_length=100)),
                ('facility_location', models.CharField(default='Kenya', max_length=100)),
                ('facility_level', models.CharField(default='2', max_length=10)),
                ('facility_phone', models.CharField(max_length=15)),
                ('facility_phone2', models.CharField(max_length=15, null=True)),
                ('facility_phone3', models.CharField(max_length=15, null=True)),
                ('facility_email', models.CharField(max_length=100)),
                ('facility_address', models.CharField(max_length=100, null=True)),
                ('facility_website', models.URLField(null=True)),
                ('facility_logo', models.ImageField(default='logo.png', upload_to=base.models.upload_path_handler)),
                ('created', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
