# Generated by Django 4.1.5 on 2023-07-12 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_alter_payroll_from_date_alter_payroll_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='to_date',
            field=models.DateField(),
        ),
    ]