# Generated by Django 4.1.5 on 2023-07-09 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_rename_service_lablog_service_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_id', models.CharField(max_length=10, unique=True)),
                ('check_in_time', models.TimeField(auto_now_add=True)),
                ('check_out_time', models.TimeField(null=True)),
                ('remarks', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('national_id', models.IntegerField(default=0)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('residence', models.CharField(max_length=50)),
                ('active_status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.department')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc_id', models.CharField(max_length=10, unique=True)),
                ('account_name', models.CharField(max_length=100, unique=True)),
                ('account_description', models.TextField()),
                ('amount_available', models.FloatField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_id', models.CharField(max_length=10, unique=True)),
                ('from_date', models.DateTimeField(auto_now_add=True)),
                ('to_date', models.DateTimeField(null=True)),
                ('remarks', models.TextField()),
                ('amount_payable', models.IntegerField(default=0)),
                ('serial_code', models.CharField(max_length=50, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.employee')),
                ('mode_of_payment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.paymentmode')),
                ('payer_account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.financialaccount')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type_id', models.CharField(max_length=10, unique=True)),
                ('leave_type', models.CharField(max_length=30, unique=True)),
                ('leave_description', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_id', models.CharField(max_length=10, unique=True)),
                ('status_code', models.IntegerField(default=0)),
                ('status_description', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_id', models.CharField(max_length=10, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_description', models.TextField()),
                ('employer_remarks', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.employee')),
                ('leave_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.leavetype')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.leavestatus')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evl_id', models.CharField(max_length=10, unique=True)),
                ('evaluation_time', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField()),
                ('efficiency_index', models.FloatField(default=1.0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('attendance_logs', models.ManyToManyField(blank=True, to='base.attendancelog')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.employee')),
                ('leaves_taken', models.ManyToManyField(blank=True, to='base.employeeleave')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='attendancelog',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.employee'),
        ),
        migrations.AddField(
            model_name='attendancelog',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
