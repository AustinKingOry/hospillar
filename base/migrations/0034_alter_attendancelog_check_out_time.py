# Generated by Django 4.1.5 on 2023-07-09 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_attendancelog_employee_financialaccount_payroll_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancelog',
            name='check_out_time',
            field=models.DateTimeField(null=True),
        ),
    ]