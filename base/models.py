from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
import datetime
from django.utils import timezone

def upload_path_handler(instance, filename):
    return "uploads/user_{id}/{file}".format(id=instance.id, file=filename)

def upload_path_handler_fac(instance, filename):
    return "facilities/facility_{id}/{file}".format(id=instance.id, file=filename)

# system models
class Facility(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    facility_name = models.CharField(max_length=100,default="Hospillar M.S")
    facility_location = models.CharField(max_length=100,default="Kenya")
    facility_level = models.CharField(max_length=10,default="2")
    facility_phone = models.CharField(max_length=15)
    facility_phone2 = models.CharField(max_length=15,null=True,blank=True)
    facility_phone3 = models.CharField(max_length=15,null=True,blank=True)
    facility_email = models.CharField(max_length=100)
    facility_address = models.CharField(max_length=100,null=True)
    facility_website = models.URLField(null=True,blank=True)
    facility_logo = models.ImageField(upload_to=upload_path_handler_fac,default='logo.png')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User',on_delete=models.SET_NULL,null=True)
    
    def __str__(self)->str:
        return self.facility_name
    
    def field_id(self):
        return self.rec_id
    
class Department(models.Model):
    role_0 = 'null'
    role_1 = 'consultation'
    role_2 = 'pharmacy'
    role_3 = 'nursing'
    role_4 = 'cashier'
    role_5 = 'hr'
    role_6 = 'laboratory'
    role_7 = 'imaging'
    role_8 = 'dental'
    role_9 = 'I.T'
    role_10 = 'sales'
    role_11 = 'finance'
    departmental_roles = [
        (role_0,'None'),
        (role_1,'consultation'),
        (role_2,'pharmacy'),
        (role_3,'nursing'),
        (role_4,'cashier'),
        (role_5,'human resource'),
        (role_6,'laboratory'),
        (role_7,'sonography & imaging'),
        (role_8,'dental services'),
        (role_9,'I.T'),
        (role_10,'sales & marketing'),
        (role_11,'finance'),
    ]
    rec_id=models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=50,null=False,default='Doctor')
    handles_patient = models.BooleanField(default=False)
    handles_drugs = models.BooleanField(default=False,help_text="This should only be activated for pharmacy.")
    role = models.CharField(max_length=50,choices=departmental_roles,default=role_0)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.name
    def field_id(self):
        return self.rec_id

class EmergencyCode(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    code_name = models.CharField(max_length=15,unique=True)
    code_number = models.IntegerField(default=0)
    code_responders = models.ManyToManyField(Department)
    code_description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey('User',on_delete=models.SET_NULL,null=True)
    
    def __str__(self) -> str:
        return self.code_name
    
    def field_id(self):
        return self.rec_id

class User(AbstractUser):
    userId = models.CharField(max_length=10,unique=True)
    access_level = models.IntegerField(null=False,default=2,blank=True)
    department = models.ForeignKey(Department,null=True,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to=upload_path_handler,default='avatar.png')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-created']
    def __str__(self)->str:
        return self.username
    def field_id(self):
        return self.userId
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

class Drug(models.Model):
    drugId = models.CharField(max_length=10,unique=True)
    drug_name = models.CharField(max_length=100,null=False,default='Unnamed')
    quantity = models.IntegerField(null=False,default=0)
    buying_price = models.IntegerField()
    selling_price = models.IntegerField()
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    expiry_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.drug_name
    def field_id(self):
        return self.drugId

class DrugStockTake(models.Model):
    recId = models.CharField(max_length=10,unique=True)
    drug = models.ForeignKey(Drug,on_delete=models.DO_NOTHING)
    existing_quantity = models.IntegerField(null=False,default=0)
    new_quantity = models.IntegerField(null=False,default=0)
    buying_price = models.IntegerField()
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    expiry_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.drug.drug_name
    def field_id(self):
        return self.recId
    def created_today(self):
        current_date = timezone.localdate()
        stored_date = self.created.astimezone(timezone.get_current_timezone()).date()
        return current_date == stored_date
    
class Service(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    service_name = models.CharField(max_length=100)
    service_charge = models.IntegerField()
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    service_group = models.CharField(max_length=30,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.service_name
    def field_id(self):
        return self.rec_id
    
class PaymentMode(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    mode_name = models.CharField(max_length=50)
    mode_class = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.mode_name
    def field_id(self):
        return self.rec_id
    
class PayerScheme(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    payer_name = models.CharField(max_length=50)
    payer_class = models.ForeignKey(PaymentMode,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.payer_name
    def field_id(self):
        return self.rec_id
    
class Patient(models.Model):
    adm_1 = 'OUTPATIENT'
    adm_2 = 'INPATIENT'
    admission_choices = [
        (adm_1,'outpatient'),
        (adm_2,'inpatient'),
    ]
    patId = models.CharField(max_length=10,null=True,unique=True)
    op_number = models.CharField(max_length=10,null=True,unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.IntegerField(blank=False,null=False,default=00000000)
    admission_category = models.CharField(max_length=15,null=False,choices=admission_choices,default=adm_1)
    phone = models.CharField(max_length=15,null=False)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=False)
    marital_status = models.CharField(max_length=15)
    companion = models.CharField(max_length=100,null=True)
    companion_phone = models.CharField(max_length=15,null=True)
    companion_relationship = models.CharField(max_length=20,null=True)
    residence = models.CharField(max_length=50)
    service = models.ForeignKey(Service,on_delete=models.SET_NULL,null=True)
    payment_mode = models.ForeignKey(PayerScheme,on_delete=models.SET_NULL,null=True)
    visit_type = models.CharField(max_length=50,default='General')   
    visit_number = models.IntegerField(auto_created=True,default=1)
    active_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # def __str__(self) -> str:
    #     return self.first_name+' '+self.middle_name+' '+self.last_name
    def full_name(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    def __str__(self) -> str:
        return self.full_name()
    def field_id(self):
        return self.patId
    def field_op(self):
        return self.op_number
    
class Prescription(models.Model):
    prcp_id = models.CharField(max_length=10,unique=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    patlog = models.ForeignKey('PatientLog',on_delete=models.SET_NULL,null=True,related_name='pre_patlog')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    drug = models.ForeignKey(Drug,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_amount = models.FloatField(default=0)
    dosage = models.CharField(max_length=10)
    frequency = models.CharField(max_length=5)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.drug.drug_name
    def field_id(self):
        return self.prcp_id
    def get_total_price(self)->float:
            return self.price*self.quantity
    
class ServiceLog(models.Model):
    sl_id = models.CharField(max_length=10,unique=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    patient_log = models.ForeignKey('PatientLog',on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    service = models.ForeignKey(Service,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_amount = models.FloatField(default=0)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.service.service_name
    def field_id(self):
        return self.sl_id
    def get_total_price(self)->float:
            return self.price*self.quantity


class PatientLog(models.Model):
    adm_1 = 'OUTPATIENT'
    adm_2 = 'INPATIENT'
    admission_choices = [
        (adm_1,'outpatient'),
        (adm_2,'inpatient'),
    ]
    patlog_id = models.CharField(max_length=10,unique=True)
    admission_category = models.CharField(max_length=15,null=False,choices=admission_choices,default=adm_1)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,null=False)
    doctor = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    emergency_code = models.ForeignKey(EmergencyCode,on_delete=models.SET_NULL,null=True,blank=True)
    payment_mode = models.ForeignKey(PayerScheme,on_delete=models.SET_NULL,null=True)
    body_temp = models.CharField(max_length=7)
    weight = models.CharField(max_length=5)
    blood_pressure = models.CharField(max_length=5)
    height = models.CharField(max_length=5)
    med_history = models.TextField()
    symptoms = models.TextField()
    test_results = models.TextField(default="None")
    recommendations = models.TextField()
    impression = models.TextField()
    additional_notes = models.TextField()
    prescription = models.ManyToManyField(Prescription,blank=True,related_name='drug_prescription')
    inclusive_service = models.ManyToManyField(ServiceLog,blank=True)
    current_stage = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name="cur_dept")
    active_status = models.BooleanField(default=False)
    involved_depts = models.ManyToManyField(Department,blank=True)
    total_charge = models.FloatField(default=0,null=True,blank=True)
    med_cleared = models.BooleanField(default=False)
    cash_cleared = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self)->str:
        return self.patient.full_name()
    def field_id(self):
        return self.patlog_id
    # def created_today(self):
    #     d = datetime.date.today()
    #     storedDate = self.created
    #     return (d.year+d.month+d.day) == (storedDate.year+storedDate.month+storedDate.day)
    def created_today(self):
        current_date = timezone.localdate()  # Get the current date in the current timezone
        stored_date = self.created.astimezone(timezone.get_current_timezone()).date()  # Convert stored datetime to current timezone and extract date
        return current_date == stored_date

# still to decide the necessity of this. It does not seem to serve any purpose
class ServiceAndPrescriptionLog(models.Model):
    spl_id = models.CharField(max_length=10,unique=True)
    patient_log = models.ForeignKey(PatientLog,on_delete=models.SET_NULL,null=True)
    services = models.ForeignKey(ServiceLog,on_delete=models.SET_NULL,null=True)
    prescriptions = models.ForeignKey(Prescription,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.patient_log.patient.full_name()
    def field_id(self):
        return self.spl_id
    
    
class LabLog(models.Model):
    lab_log_id = models.CharField(max_length=10,unique=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    service_log = models.ForeignKey(ServiceLog,models.SET_NULL,null=True)
    quantity = models.IntegerField()
    pat_log = models.ForeignKey(PatientLog,on_delete=models.CASCADE)
    findings = models.TextField()
    cleared = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.service_log.service.service_name
    def field_id(self):
        return self.lab_log_id
        
class ImagingLog(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    service_log = models.ForeignKey(ServiceLog,models.SET_NULL,null=True)
    quantity = models.IntegerField()
    pat_log = models.ForeignKey(PatientLog,on_delete=models.CASCADE)
    results = models.TextField()
    cleared = models.BooleanField(default=False)
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.service_log.service.service_name
    def field_id(self):
        return self.rec_id
            
class DentalLog(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    service_log = models.ForeignKey(ServiceLog,models.SET_NULL,null=True)
    quantity = models.IntegerField()
    pat_log = models.ForeignKey(PatientLog,on_delete=models.CASCADE)
    results = models.TextField()
    cleared = models.BooleanField(default=False)
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.service_log.service.service_name
    def field_id(self):
        return self.rec_id
    
class CashOption(models.Model):
    rec_id=models.CharField(max_length=10,unique=True)
    option_name = models.CharField(max_length=50)
    parent_payer = models.ForeignKey(PayerScheme,on_delete=models.CASCADE)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.option_name
    def field_id(self):
        return self.rec_id
    
class DebitPaymentLog(models.Model):
    dpy_id = models.CharField(max_length=20,unique=True)
    pat_log = models.ForeignKey(PatientLog,on_delete=models.CASCADE)
    billable_amount = models.IntegerField(null=False,default=0)
    payer = models.ForeignKey(PayerScheme,on_delete=models.SET_NULL,null=True)
    cash_option = models.ForeignKey(CashOption,on_delete=models.SET_NULL,null=True)
    cash_value = models.IntegerField(null=False,default=0)
    epay_value = models.IntegerField(null=False,default=0)
    invoice_value = models.IntegerField(null=False,default=0)
    balance = models.IntegerField(null=False,default=0)
    transaction_code = models.CharField(max_length=100,null=True)
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->str:
        return self.pat_log.patient.full_name()
    def field_id(self):
        return self.dpy_id
    def calc_bal(self):
        return (self.billable_amount)-(self.cash_value+self.epay_value+self.invoice_value)
    
class Employee(models.Model):
    employee_id = models.CharField(max_length=10,unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.IntegerField(blank=False,null=False,default=00000000)
    phone = models.CharField(max_length=15,null=False)
    email = models.CharField(max_length=100,null=True,default='N/A',blank=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=False)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    residence = models.CharField(max_length=50)
    active_status = models.BooleanField(default=False)
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def full_name(self) -> str:
        return self.first_name+' '+self.middle_name+' '+self.last_name
    def __str__(self) -> str:
        return self.full_name()
    def field_id(self):
        return self.employee_id

class LeaveStatus(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    status_code = models.IntegerField(default=0)
    status_description = models.CharField(max_length=20)
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.status_description
    def field_id(self):
        return self.rec_id
    
    '''
    pending-1
    approved-2
    rejected-3
    on session/ongoing-4
    expired-5
    '''
        
class LeaveType(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    leave_type = models.CharField(max_length=30,unique=True)
    leave_description = models.CharField(max_length=50)
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.leave_type
    def field_id(self):
        return self.rec_id
    
class EmployeeLeave(models.Model):
    leave_id = models.CharField(max_length=10,unique=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.ForeignKey(LeaveType,on_delete=models.SET_NULL,null=True)
    leave_description = models.TextField()
    employer_remarks = models.TextField()
    status = models.ForeignKey(LeaveStatus,on_delete=models.SET_NULL,null=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.employee.full_name()
    
    def field_id(self):
        return self.leave_id
    
class AttendanceLog(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True)
    remarks = models.TextField()
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.employee.full_name()
    
    def field_id(self):
        return self.rec_id

class EmployeeEvaluation(models.Model):
    evl_id = models.CharField(max_length=10,unique=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    evaluation_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField()
    attendance_logs = models.ManyToManyField(AttendanceLog,blank=True)
    leaves_taken = models.ManyToManyField(EmployeeLeave,blank=True)
    efficiency_index = models.FloatField(default=1.0)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.employee.full_name()
    
    def field_id(self):
        return self.evl_id
    
class FinancialAccount(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    account_name = models.CharField(max_length=100,unique=True)
    account_description = models.TextField()
    amount_available = models.FloatField(default=0)
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.account_name
    
    def field_id(self):
        return self.rec_id
    
class Payroll(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    amount_payable = models.IntegerField(default=0)
    mode_of_payment = models.ForeignKey(PaymentMode,on_delete=models.DO_NOTHING)
    serial_code = models.CharField(max_length=50,unique=True)
    payer_account = models.ForeignKey(FinancialAccount,on_delete=models.DO_NOTHING)
    remarks = models.TextField()
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    cleared = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.employee.full_name()
    
    def field_id(self):
        return self.rec_id   
    
class Supplier(models.Model):
    rec_id = models.CharField(max_length=10,unique=True)
    supplier_name = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    description = models.TextField()
    added_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.supplier_name
    
    def field_id(self):
        return self.rec_id