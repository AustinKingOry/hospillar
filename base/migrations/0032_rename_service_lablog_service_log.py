# Generated by Django 4.1.5 on 2023-07-07 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_remove_lablog_patient_lablog_cleared_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lablog',
            old_name='service',
            new_name='service_log',
        ),
    ]