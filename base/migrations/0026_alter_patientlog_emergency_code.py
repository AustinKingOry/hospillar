# Generated by Django 4.1.5 on 2023-07-06 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_alter_facility_facility_phone2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientlog',
            name='emergency_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.emergencycode'),
        ),
    ]
