# Generated by Django 4.1.5 on 2023-07-20 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_rename_user_emergencycode_added_by_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='generates_income',
            field=models.BooleanField(default=False),
        ),
    ]