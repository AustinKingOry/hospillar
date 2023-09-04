from django.contrib import admin
from .models import User,Patient,PatientLog,PaymentMode,Prescription,Department,Drug,Service,LabLog,PayerScheme,ServiceLog,DebitPaymentLog,CashOption,DrugStockTake,Facility,EmergencyCode,Employee,LeaveStatus,LeaveType,EmployeeLeave,AttendanceLog,EmployeeEvaluation,FinancialAccount,Payroll,ImagingLog,Supplier,DentalLog
# Register your models here.

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(PatientLog)
admin.site.register(PaymentMode)
admin.site.register(Prescription)
admin.site.register(Department)
admin.site.register(Drug)
admin.site.register(Service)
admin.site.register(LabLog)
admin.site.register(PayerScheme)
admin.site.register(ServiceLog)
admin.site.register(DebitPaymentLog)
admin.site.register(CashOption)
admin.site.register(DrugStockTake)
admin.site.register(Facility)
admin.site.register(EmergencyCode)
admin.site.register(Employee)
admin.site.register(LeaveStatus)
admin.site.register(LeaveType)
admin.site.register(EmployeeLeave)
admin.site.register(AttendanceLog)
admin.site.register(EmployeeEvaluation)
admin.site.register(FinancialAccount)
admin.site.register(Payroll)
admin.site.register(ImagingLog)
admin.site.register(Supplier)
admin.site.register(DentalLog)