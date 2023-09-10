from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm,PasswordResetForm
from .models import Patient,User,PatientLog,Prescription,ServiceLog,DebitPaymentLog,Drug,DrugStockTake,Employee,EmployeeEvaluation,AttendanceLog,EmployeeLeave,Payroll,Department,Service,PayerScheme,PaymentMode,EmergencyCode,Facility,CashOption,LeaveStatus,LeaveType,FinancialAccount,ImagingLog,Supplier,Appointment
from django.contrib.auth.models import Group

class MyUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'phone', 'access_level', 'department', 'gender', 'profile_photo','groups']
     
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['profile_photo', 'first_name', 'last_name', 'email', 'phone']
        exclude = ['password1','password2']
       
class ChangePwdForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']
        
class ForgotPwdForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        # fields = '__all__'
        fields = ['first_name','middle_name','last_name','national_id','admission_category','phone','gender','date_of_birth','marital_status','companion','companion_phone','companion_relationship','residence','service','payment_mode','visit_type']
        
class PatientLogForm(ModelForm):
    class Meta:
        model = PatientLog
        fields = '__all__'
        exclude = ['patlog_id','active_status','created','patient','doctor','payment_mode','prescription','inclusive_service']
        
class NursePatientLogForm(ModelForm):
    class Meta:
        model = PatientLog
        fields = ['body_temp','weight','blood_pressure','height','additional_notes','current_stage']
        
class CashPatientLogForm(ModelForm):
    class Meta:
        model = PatientLog
        fields = ['current_stage']
        
class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = ['drug','quantity','price','dosage','frequency']
        
class ServiceLogForm(ModelForm):
    class Meta:
        model = ServiceLog
        fields = ['service','quantity','price']
        
class DebitPayLogForm(ModelForm):
    class Meta:
        model = DebitPaymentLog
        fields = ['billable_amount','payer','cash_option','cash_value','epay_value','invoice_value','transaction_code']
        
class DebitPayLogFormInv(ModelForm):
    class Meta:
        model = DebitPaymentLog
        fields = ['billable_amount','payer','invoice_value','transaction_code']
        
class PharPatientLogForm(ModelForm):
    class Meta:
        model = PatientLog
        fields = ['current_stage']
        
class PharNewDrugForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['drug_name','quantity','buying_price','selling_price']
        
class PharDrugAdjustForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['drug_name','quantity','buying_price','selling_price']
        
class StockTakeForm(ModelForm):
    class Meta:
        model = DrugStockTake
        fields = ['drug','existing_quantity','new_quantity','buying_price','expiry_date']
        
class LabPatientLogForm(ModelForm):
    class Meta:
        model = PatientLog
        fields = ['current_stage','test_results']
        
class ImagingPatientLogForm(ModelForm):
    class Meta:
        model = PatientLog
        fields = ['current_stage','test_results']
        
class DentalPatientLogForm(ModelForm):
    class Meta:
        model = PatientLog
        fields = ['current_stage','test_results']
        
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['employee_id']
        
class EmployeeEvaluationForm(ModelForm):
    class Meta:
        model = EmployeeEvaluation
        fields = '__all__'
        exclude = ['evl_id','added_by','employee']
        
class EmployeeAttendanceForm(ModelForm):
    class Meta:
        model = AttendanceLog
        fields = ['employee','check_in_time','remarks']
        
class EmployeeCheckoutForm(ModelForm):
    class Meta:
        model = AttendanceLog
        fields = ['employee','check_in_time','remarks','check_out_time']
        
class LeaveStatusForm(ModelForm):
    class Meta:
        model = LeaveStatus
        fields = '__all__'
        exclude = ['rec_id','added_by']
        
class LeaveTypeForm(ModelForm):
    class Meta:
        model = LeaveType
        fields = '__all__'
        exclude = ['rec_id','added_by']
        
class EmployeeLeaveApprovalForm(ModelForm):
    class Meta:
        model = EmployeeLeave
        fields = ['employer_remarks','status']
        
class EmployeeLeaveApplicationForm(ModelForm):
    class Meta:
        model = EmployeeLeave
        fields = '__all__'
        exclude = ['employer_remarks','status','leave_id','added_by']
        
class PayrollForm(ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'
        exclude = ['rec_id','added_by','cleared']
        
class PayrollApprovalForm(ModelForm):
    class Meta:
        model = Payroll
        fields = ['cleared']
        
class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['rec_id']

class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['rec_id']
        
class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        fields = '__all__'
        exclude = ['rec_id','user']
        
class CreditorForm(ModelForm):
    class Meta:
        model = PayerScheme
        fields = '__all__'
        exclude = ['rec_id']
        
class PaymentModeForm(ModelForm):
    class Meta:
        model = PaymentMode
        fields = '__all__'
        exclude = ['rec_id']
        
class FinancialAccountForm(ModelForm):
    class Meta:
        model = FinancialAccount
        fields = '__all__'
        exclude = ['rec_id','added_by']
        
class CashOptionForm(ModelForm):
    class Meta:
        model = CashOption
        fields = '__all__'
        exclude = ['rec_id','added_by']
        
class EmergencyCodeForm(ModelForm):
    class Meta:
        model = EmergencyCode
        fields = '__all__'
        exclude = ['rec_id','added_by']
        
class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ['rec_id','added_by']
        
class DeleteForm(forms.Form):
    confirm_deletion = forms.BooleanField(widget=forms.HiddenInput)

class AddUsersToGroupForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        exclude = ['apt_id','added_by','viewed','cleared']

class AppointmentChangeForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        exclude = ['apt_id','added_by']
