# Generated by Django 4.1.5 on 2023-07-10 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_alter_attendancelog_check_in_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancelog',
            name='check_out_time',
            field=models.TimeField(null=True),
        ),
    ]