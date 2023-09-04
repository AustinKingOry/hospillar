# Generated by Django 4.1.5 on 2023-06-17 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_department_departmentid_alter_drug_drugid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='visit',
        ),
        migrations.AddField(
            model_name='prescription',
            name='patlog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pre_patlog', to='base.patientlog'),
        ),
    ]
