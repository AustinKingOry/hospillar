# Generated by Django 4.1.5 on 2023-09-07 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_alter_patientlog_total_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientlog',
            name='total_charge',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
