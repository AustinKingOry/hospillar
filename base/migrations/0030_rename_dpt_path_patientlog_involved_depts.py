# Generated by Django 4.1.5 on 2023-07-07 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_remove_patientlog_pharmacy_cleared_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientlog',
            old_name='dpt_path',
            new_name='involved_depts',
        ),
    ]
