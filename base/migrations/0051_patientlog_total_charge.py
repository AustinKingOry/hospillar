# Generated by Django 4.1.5 on 2023-09-07 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0050_rename_generates_income_department_handles_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientlog',
            name='total_charge',
            field=models.IntegerField(default=0),
        ),
    ]
