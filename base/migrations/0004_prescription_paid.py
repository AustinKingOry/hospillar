# Generated by Django 4.1.5 on 2023-06-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_prescription_visit_prescription_patlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
