# Generated by Django 4.1.5 on 2023-07-21 23:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_department_generates_income'),
    ]

    operations = [
        migrations.CreateModel(
            name='DentalLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_id', models.CharField(max_length=10, unique=True)),
                ('quantity', models.IntegerField()),
                ('results', models.TextField()),
                ('cleared', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('pat_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patientlog')),
                ('service_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.servicelog')),
            ],
        ),
    ]