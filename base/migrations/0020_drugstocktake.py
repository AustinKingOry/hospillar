# Generated by Django 4.1.5 on 2023-07-01 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_patientlog_cash_cleared'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugStockTake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recId', models.CharField(max_length=10, unique=True)),
                ('existing_quantity', models.IntegerField(default=0)),
                ('new_quantity', models.IntegerField(default=0)),
                ('buying_price', models.IntegerField()),
                ('expiry_date', models.DateField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.drug')),
            ],
        ),
    ]
