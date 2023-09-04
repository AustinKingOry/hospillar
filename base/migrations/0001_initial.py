# Generated by Django 4.1.5 on 2023-06-17 10:59

import base.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userId', models.CharField(max_length=10)),
                ('access_level', models.IntegerField(blank=True, default=2)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=50)),
                ('profile_photo', models.ImageField(default='avatar.png', upload_to=base.models.upload_path_handler)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentId', models.CharField(max_length=10)),
                ('name', models.CharField(default='Doctor', max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drugId', models.CharField(max_length=10)),
                ('drug_name', models.CharField(default='Unnamed', max_length=100)),
                ('quantity', models.IntegerField(default=0)),
                ('buying_price', models.IntegerField()),
                ('selling_price', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_number', models.IntegerField(auto_created=True, default=1)),
                ('patId', models.CharField(max_length=10, null=True, unique=True)),
                ('op_number', models.CharField(max_length=10, null=True, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('national_id', models.IntegerField(default=0)),
                ('admission_category', models.CharField(default='OP', max_length=15)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('marital_status', models.CharField(max_length=15)),
                ('companion', models.CharField(max_length=100, null=True)),
                ('companion_phone', models.CharField(max_length=15, null=True)),
                ('companion_relationship', models.CharField(max_length=20, null=True)),
                ('residence', models.CharField(max_length=50)),
                ('visit_type', models.CharField(default='General', max_length=50)),
                ('active_status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patlog_id', models.CharField(max_length=10)),
                ('body_temp', models.CharField(max_length=7)),
                ('weight', models.CharField(max_length=5)),
                ('blood_pressure', models.CharField(max_length=5)),
                ('height', models.CharField(max_length=5)),
                ('med_history', models.TextField()),
                ('symptoms', models.TextField()),
                ('recommendations', models.TextField()),
                ('impression', models.TextField()),
                ('additional_notes', models.TextField()),
                ('active_status', models.BooleanField(default=False)),
                ('med_cleared', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('current_stage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.department')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modeId', models.CharField(max_length=10)),
                ('mode_name', models.CharField(max_length=50)),
                ('mode_class', models.CharField(max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prcp_id', models.CharField(max_length=10)),
                ('visit', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('dosage', models.CharField(max_length=10)),
                ('frequency', models.CharField(max_length=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('drug', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.drug')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patient')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serviceId', models.CharField(max_length=10)),
                ('service_name', models.CharField(max_length=100)),
                ('service_charge', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.department')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sl_id', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patient')),
                ('patient_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.patientlog')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.service')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAndPrescriptionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spl_id', models.CharField(max_length=10, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('patient_log', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.patientlog')),
                ('prescriptions', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.prescription')),
                ('services', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.servicelog')),
            ],
        ),
        migrations.CreateModel(
            name='PayerScheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payerId', models.CharField(max_length=10)),
                ('payer_name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('payer_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.paymentmode')),
            ],
        ),
        migrations.AddField(
            model_name='patientlog',
            name='inclusive_service',
            field=models.ManyToManyField(blank=True, to='base.servicelog'),
        ),
        migrations.AddField(
            model_name='patientlog',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patient'),
        ),
        migrations.AddField(
            model_name='patientlog',
            name='payment_mode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.payerscheme'),
        ),
        migrations.AddField(
            model_name='patientlog',
            name='prescription',
            field=models.ManyToManyField(blank=True, related_name='drug_prescription', to='base.prescription'),
        ),
        migrations.AddField(
            model_name='patient',
            name='payment_mode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.payerscheme'),
        ),
        migrations.AddField(
            model_name='patient',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.service'),
        ),
        migrations.CreateModel(
            name='LabLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_log_id', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('findings', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pat_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patientlog')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.patient')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.service')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
