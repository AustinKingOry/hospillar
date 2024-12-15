from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group, Permission
from .forms import PatientForm,MyUserCreationForm,PatientLogForm,NursePatientLogForm,PrescriptionForm,ServiceLogForm,CashPatientLogForm,DebitPayLogForm,DebitPayLogFormInv,PharPatientLogForm,PharNewDrugForm,PharDrugAdjustForm,StockTakeForm,LabPatientLogForm,EmployeeForm,EmployeeEvaluationForm,EmployeeAttendanceForm,EmployeeCheckoutForm,EmployeeLeaveApprovalForm,EmployeeLeaveApplicationForm,PayrollForm,PayrollApprovalForm,DepartmentForm,FacilityForm,FinancialAccountForm,PaymentModeForm,CreditorForm,EmergencyCodeForm,CashOptionForm,ServiceForm,DeleteForm,LeaveStatusForm,LeaveTypeForm,ImagingPatientLogForm,SupplierForm,DentalPatientLogForm,AddUsersToGroupForm,UserUpdateForm,ChangePwdForm,ForgotPwdForm,AppointmentForm,AppointmentChangeForm,ExpenseForm,ExpenseCategoryForm,WardForm,InpatientForm

from .models import User,Department,Patient,PatientLog,PaymentMode,Service,ServiceLog,Drug,PayerScheme,Prescription,DebitPaymentLog,DrugStockTake,EmergencyCode,Facility,LabLog,Employee,EmployeeEvaluation,AttendanceLog,EmployeeLeave,LeaveStatus,LeaveType,Payroll,CashOption,FinancialAccount,ImagingLog,Supplier,DentalLog,Appointment,ExpenseCategory,Expense,Ward,Inpatient
from .functions import createId,createPrescription,createServiceLog,createOp,create_groups,is_admin,user_perms,has_custom_permissions,daily_departmental_income,daily_pharmacy_income,daily_inpatient_by_dpt,daily_outpatient_by_dpt,daily_income_by_dpt
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
import datetime

# Create your views here.
@login_required(login_url="login")
def home(request):
    collections = {}
    dpt_collections = {}
    total_collection = 0
    current_date = timezone.localdate()
    today_services = ServiceLog.objects.filter(created__date = current_date)[0:15]
    patient_files = PatientLog.objects.filter(created__date=current_date)[0:20]
    all_appointments = Appointment.objects.filter(cleared=False,appointment_date=current_date).order_by('name')
    expenses = Expense.objects.filter(created__date=current_date)
    total_expenses = 0
    for e in expenses:
        total_expenses += e.amount
    # getting the sum total income for all payers
    paylogs = DebitPaymentLog.objects.filter(created__date=current_date)
    for p in paylogs:
        if not p.payer in collections:
            collections[str(p.payer)]=p.billable_amount
            total_collection+=p.billable_amount
        else:
            collections[str(p.payer)]+=p.billable_amount
            total_collection+=p.billable_amount
    # getting the total income for every department
    for dpt in Department.objects.filter(handles_patient=True):
        if not dpt.role in dpt_collections:
            if not dpt.handles_drugs:
                dpt_collections[str(dpt.role)]=daily_departmental_income(dpt)
            else:
                dpt_collections[str(dpt.role)]=daily_pharmacy_income()
    page_title = 'Dashboard'
    context = {'page_title':page_title,'total_expenses':total_expenses,'patient_files':patient_files,'today_services':today_services,'collections':collections,'dpt_collections':dpt_collections,'total_collection':total_collection,'appointments':all_appointments,'daily_dpt_income':daily_income_by_dpt()}
    return render(request,'base/home.html',context)

def no_permission(request):
    page_title = 'Not Authorized.'
    context = {'page_title':page_title}
    return render(request,'base/no-permission.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def hospAdmin(request):
    page_title = 'Hospillar Admin'
    context = {'page_title':page_title}
    return render(request,'base/admin/admin.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def addUser(request):
    form = MyUserCreationForm()
    departments = Department.objects.all()
    groups = Group.objects.all()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            perm_groups = request.POST.getlist('groups')
            user = form.save(commit=False)
            user.userId = str(createId(User,User.userId,'OHU'))
            user.save()
            user.groups.set(form.cleaned_data['groups'])
            messages.success(request,'Account created successfully.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    
    page_title = 'Admin | Add User'
    context = {'page_title':page_title,'form':form,'departments':departments,'groups':groups}
    return render(request,'base/admin/add-user.html',context)

@login_required(login_url="login")
def editProfile(request):
    user = User.objects.get(id=request.user.id)
    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Account updated successfully.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    
    page_title = 'Edit Profile'
    context = {'page_title':page_title,'form':form}
    return render(request,'base/edit-profile.html',context)

@login_required(login_url='signin')
def change_password(request):
    try:
        user = User.objects.get(id=request.user.id)
    except:
        return
    form = ChangePwdForm(user)
    if request.method == 'POST':
        form = ChangePwdForm(user,request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Password has been changed successfully.')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Change Password'
    context = {'page_title':page_title,'form':form}
    return render(request,'base/change-password.html',context)

def forgot_password(request):
    form = ForgotPwdForm()
    if request.method == 'POST':
        form = ForgotPwdForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Check your email for a one-time link for reseting your password.')
            # return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Change Password'
    context = {'page_title':page_title,'form':form,'hide_skeleton':True}
    return render(request,'base/forgot-password.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def usersList(request):
    users = User.objects.all()
    page_title = 'User Accounts'
    context = {'page_title':page_title,'users':users}
    return render(request,'base/admin/users-list.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def patientLogsList(request):
    files = PatientLog.objects.all()
    records_list=[] 
    for s in files:
        sub=[]
        sub.append(s.id)
        sub.append(s.patient.op_number)
        sub.append(s.patient.full_name())
        sub.append(s.patlog_id)
        sub.append(s.created.date)
        records_list.append(sub)
    keyword = 'patient_log_file'
    fields = {'#':'id','OP Number':'patient.op_number','Patient Name':'patient.full_name','File No.':'patlog_id','Date':'created'}
    page_title = 'Patient Log Files'
    context = {'page_title':page_title,'records_list':records_list,'files':files,'keyword':keyword,'fields':fields}
    return render(request,'base/admin/patients-list.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def AdminPatientLogFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    drugs = Drug.objects.all()
    patientLogFile = PatientLog.objects.get(id=pk)
    prev_files =[]
    for file in PatientLog.objects.filter(patient=patientLogFile.patient,active_status=False):
        if not file==patientLogFile:
            prev_files.append(file)
    services = patientLogFile.inclusive_service.all()
    prescriptions = patientLogFile.prescription.all()
    form = PatientLogForm(instance=patientLogFile)
    page_title = 'Med Patient File'
    context = {'page_title':page_title,'form':form,'patientlog':patientLogFile,'services':services,'departments':departments,'drugs':drugs,'prescriptions':prescriptions,'prev_files':prev_files}
    return render(request,'base/admin/patient-log-file.html',context)

def hospLogin(request):
    if(request.method=='POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Account does not exist!')
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"Welcome back, "+str(user))
            return redirect('home')
            # return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request,'Incorrect username/password combination!')
            
    page_title = 'Signin'
    context = {'page_title':page_title,'hide_skeleton':True}
    return render(request,'base/login.html',context)

@login_required(login_url="login")
def hospLogout(request):
    logout(request)
    # return redirect('home')
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def reception(request):
    page_title = 'Reception Office'
    context = {'page_title':page_title}
    return render(request,'base/reception/reception.html',context)

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def reception_pat_inventory(request):
    all_patients = Patient.objects.all().order_by('first_name')
    page_title = 'Patients Inventory'
    context = {'page_title':page_title,'patients':all_patients}
    return render(request,'base/reception/all-patients.html',context)

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def reception_daily_patients(request):
    current_date = timezone.localdate()
    patient_files = PatientLog.objects.filter(created__date=current_date)[0:20]
    page_title = 'Patients Inventory'
    context = {'page_title':page_title,'patients':patient_files}
    return render(request,'base/reception/daily-patients.html',context)

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def reception_appointments(request):
    all_appointments = Appointment.objects.filter(cleared=False).order_by('name')
    form = AppointmentForm()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            apt = form.save(commit=False)
            apt.apt_id = createId(Appointment,Appointment.apt_id,'APT')
            apt.added_by = request.user
            apt.save()
            messages.success(request,'Appointment has been booked successfully.')
            return redirect('rec-appointments')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Appointments'
    context = {'page_title':page_title,'appointments':all_appointments,'form':form}
    return render(request,'base/reception/appointments.html',context)

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def reception_appointment_file(request,pk):
    appointment = Appointment.objects.get(id=pk)
    form = AppointmentChangeForm(instance = appointment)
    if request.method == 'POST':
        form = AppointmentChangeForm(request.POST,instance = appointment)
        if form.is_valid():
            form.save()
            messages.success(request,'Appointment has been updated successfully.')
            return redirect('rec-appointments')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Appointment file'
    context = {'page_title':page_title,'appointment':appointment,'form':form}
    return render(request,'base/reception/appointment-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def rec_new_patient(request):
    form = PatientForm()
    departments = Department.objects.filter(handles_patient=True)
    emergency_codes = EmergencyCode.objects.all()
    payers = PayerScheme.objects.all()
    services = Service.objects.all()
    #getting a list of doctors from users and departments
    if Department.objects.filter(role='consultation').exists():
        docDptid = Department.objects.get(role='consultation').id
    else:
        docDptid = None
    doctors = User.objects.filter(department=docDptid)
    #getting a list of nurses from users and departments
    if Department.objects.filter(role='nursing').exists():
        nurDptid = Department.objects.get(role='nursing').id
    else:
        nurDptid = None
    nurses = User.objects.filter(department=nurDptid)
    #processing new patient data
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.visit_number = 1
            patient.patId = str(createId(Patient,Patient.patId,'PAT'))
            if request.POST.get('admission_category').lower()=='outpatient':
                patient.op_number = str(createOp(Patient,Patient.op_number,'GOP'))
            else:
                patient.op_number = str(createOp(Patient,Patient.op_number,'GIP'))
            patient.save()
            messages.success(request,'Registration was a success!')
            
            formForwardDpt = request.POST.get('forward-to-dpt')
            if Department.objects.filter(id=formForwardDpt).exists():
                forwarded_dpt = Department.objects.get(id=formForwardDpt)
            formAssignedTo = request.POST.get('assigned-user')
            if User.objects.filter(id=formAssignedTo).exists():
                assigned_user = User.objects.get(id=formAssignedTo)
            formPayMode = request.POST.get('payment_mode')
            if PayerScheme.objects.filter(id=formPayMode).exists():
                paymode = PayerScheme.objects.get(id=formPayMode)
            formEmcCode = request.POST.get('emergency_code')
            if EmergencyCode.objects.filter(id=formEmcCode).exists():
                emcCode = EmergencyCode.objects.get(id=formEmcCode)
            else:
                emcCode = None
            
            pat_log=PatientLog.objects.create(
                patlog_id = str(createId(PatientLog,PatientLog.patlog_id,'PLG')),
                patient = patient,
                doctor = assigned_user,
                payment_mode = paymode,
                current_stage = forwarded_dpt,
                admission_category = form.cleaned_data['admission_category'],
                emergency_code = emcCode,
                active_status = True,
            )
            initialService = createServiceLog(pat_log.id,request.user.id,request.POST.get('service'))
            pat_log.inclusive_service.add(initialService)
            pat_log.involved_depts.add(forwarded_dpt)
            
            if request.POST.get('admission_category').lower()=='inpatient':
                inpt_file=Inpatient.objects.create(
                    rec_id = str(createId(Inpatient,Inpatient.rec_id,'PAT')),
                    patient_file = pat_log,
                    condition = '',
                )
            return redirect('reception')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Add New Patient'
    context = {'page_title':page_title,'form':form,'payers':payers,'departments':departments,'services':services,'doctors':doctors,'emergency_codes':emergency_codes}
    return render(request,'base/reception/new-pat-form.html',context)

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def reception_search_patient(request):
    patients = None
    if request.method == 'POST':
        q = request.POST.get('search-term')
        category = (request.POST.get('search-category')).lower()
        if category == 'name':
            #modify this to search for full name
            patients = Patient.objects.filter(
                Q(first_name__icontains=q) |
                Q(middle_name__icontains=q) |
                Q(last_name__icontains=q) 
            ).order_by('first_name')
        elif category == 'op':
            patients = Patient.objects.filter(
                Q(op_number__icontains=q)
            ).order_by('first_name')
        elif category == 'tel':
            patients = Patient.objects.filter(
                Q(phone__icontains=q)
            ).order_by('first_name')
        elif category == 'id':
            patients = Patient.objects.filter(
                Q(national_id__icontains=q)
            ).order_by('first_name')
        else:
            messages.error(request,"Check your search criteria and try again!😉")
    page_title = 'Search Patient'
    context = {'page_title':page_title,'patients':patients}
    return render(request,'base/reception/search.html',context)

@login_required(login_url="login")
@permission_required(user_perms('reception'),login_url='no-permission')
def rec_show_patient(request,pk):
    patient = Patient.objects.get(id=pk)
    departments = Department.objects.filter(handles_patient=True)
    emergency_codes = EmergencyCode.objects.all()
    payers = PayerScheme.objects.all()
    services = Service.objects.all()
    form = PatientForm(instance=patient)
    #getting a list of doctors from users and departments
    if Department.objects.filter(role='consultation').exists():
        docDptid = Department.objects.get(role='consultation').id
    else:
        docDptid = None
    doctors = User.objects.filter(department=docDptid)
    #getting a list of nurses from users and departments
    if Department.objects.filter(role='nursing').exists():
        nurDptid = Department.objects.get(role='nursing').id
    else:
        nurDptid = None
    nurses = User.objects.filter(department=nurDptid)
    #processing new patient data
    if request.method == 'POST':
        form = PatientForm(request.POST,instance=patient)
        if form.is_valid():
            patientFile = form.save(commit=False)
            patientFile.visit_number += 1
            patientFile.save()
            messages.success(request,'Registration was a success!')
            
            formForwardDpt = request.POST.get('forward-to-dpt')
            if Department.objects.filter(id=formForwardDpt).exists():
                forwarded_dpt = Department.objects.get(id=formForwardDpt)
            formAssignedTo = request.POST.get('assigned-user')
            if User.objects.filter(id=formAssignedTo).exists():
                assigned_user = User.objects.get(id=formAssignedTo)
            formPayMode = request.POST.get('payment_mode')
            if PayerScheme.objects.filter(id=formPayMode).exists():
                paymode = PayerScheme.objects.get(id=formPayMode)
            formEmcCode = request.POST.get('emergency_code')
            if EmergencyCode.objects.filter(id=formEmcCode).exists():
                emcCode = EmergencyCode.objects.get(id=formEmcCode)
            else:
                emcCode = None
            
            pat_log=PatientLog.objects.create(
                patlog_id = str(createId(PatientLog,PatientLog.patlog_id,'PLG')),
                patient = patient,
                doctor = assigned_user,
                payment_mode = paymode,
                current_stage = forwarded_dpt,
                admission_category = form.cleaned_data['admission_category'],
                emergency_code = emcCode,
                active_status = True,
            )
            initialService = createServiceLog(pat_log.id,request.user.id,request.POST.get('service'))
            pat_log.inclusive_service.add(initialService)
            pat_log.involved_depts.add(forwarded_dpt)
            if request.POST.get('admission_category').lower()=='inpatient':
                inpt_file=Inpatient.objects.create(
                    rec_id = str(createId(Inpatient,Inpatient.rec_id,'PAT')),
                    patient_file = pat_log,
                    condition = '',
                )
            return redirect('reception')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Patient File | '+patient.full_name()
    context = {'page_title':page_title,'form':form,'payers':payers,'departments':departments,'services':services,'doctors':doctors,'patient':patient,'emergency_codes':emergency_codes}
    return render(request,'base/reception/patient-file.html',context)

#cash office and its related files
@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashier(request):
    page_title = 'Cash Office'
    context = {'page_title':page_title}
    return render(request,'base/cashier/cashier.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierPending(request):
    if Department.objects.filter(role='cashier').exists():
        docDptid = Department.objects.get(role='cashier').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(active_status=True,current_stage=docDptid,created__date=current_date):        
        if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Pending Payments'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/cashier/pending-payments.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierUncompleted(request):
    patientLogFiles = []
    for patlog in PatientLog.objects.filter(active_status=False,cash_cleared=False).order_by('-created'):
        patientLogFiles.append(patlog)
    page_title = 'Uncompleted Patients'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/cashier/uncompleted-payments.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierCleared(request):
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(active_status=False,cash_cleared=True,created__date=current_date).order_by('-created'):
        patientLogFiles.append(patlog)
    page_title = 'Cleared Payments'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/cashier/cleared-payments.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierPatFile(request,pk):
    patientLogFile = PatientLog.objects.get(id=pk)
    departments = Department.objects.filter(handles_patient=True)
    services = patientLogFile.inclusive_service.all()
    prescriptions = patientLogFile.prescription.all()
    form = CashPatientLogForm(instance=patientLogFile)
    # totalservices=(prescriptions.count()) + services.count()
    totalPrice = 0
    allItems = []
    for p in prescriptions:
        allItems.append(p)
        totalPrice+=(p.price*p.quantity)
    for s in services:
        allItems.append(s)
        totalPrice+=(s.price*s.quantity)
    if(request.method == 'POST'):
        form = CashPatientLogForm(request.POST,instance=patientLogFile)
        if form.is_valid():
            logfile=form.save(commit=False)
            logfile.med_cleared=False
            logfile.save()
            logfile.involved_depts.add(request.POST.get('current_stage'))
            messages.success(request,'Patient data updated successfully!')
            return redirect('cash-uncompleted')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Cash Office | Patient File'
    context = {'page_title':page_title,'form':form,'patientlog':patientLogFile,'services':services,'departments':departments,'prescriptions':prescriptions,'totalPrice':totalPrice,'allItems':allItems}
    return render(request,'base/cashier/patient-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierReceiptsList(request):
    if PayerScheme.objects.filter(payer_name='Cash Paying').exists():
        pysid = PayerScheme.objects.get(payer_name='Cash Paying').id
    paymentLogFiles = []
    if DebitPaymentLog.objects.filter(payer=pysid).exists():
        for patlog in DebitPaymentLog.objects.filter(payer=pysid).order_by('-created'):
            paymentLogFiles.append(patlog)
    page_title = 'Reprint Receipts'
    context = {'page_title':page_title,'paymentlogs':paymentLogFiles}
    return render(request,'base/cashier/cash-receipts-list.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierExpenses(request):
    current_date = timezone.localdate()
    all_expenses = Expense.objects.filter(created__date=current_date)
    form = ExpenseForm()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.rec_id=createId(Expense,Expense.rec_id,'EXP')
            exp.added_by = request.user
            exp.save()
            messages.success(request,'Expense has been added successfully.')
            return redirect('cash-petty-cash')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Petty Cash Account'
    context = {'page_title':page_title,'all_expenses':all_expenses,'form':form}
    return render(request,'base/cashier/petty-cash.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierInvoicesList(request):
    paymentLogFiles = []
    if DebitPaymentLog.objects.filter(payer__payer_class__mode_class='Invoice').exists():
        for patlog in DebitPaymentLog.objects.filter(payer__payer_class__mode_class='Invoice').order_by('-created'):
            paymentLogFiles.append(patlog)
    page_title = 'Patient Invoice List'
    context = {'page_title':page_title,'paymentlogs':paymentLogFiles}
    return render(request,'base/cashier/patient-invoice-list.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def patientInvoice(request,pk):
    paymentLogFile = DebitPaymentLog.objects.get(id=pk)
    patientLogFile = paymentLogFile.pat_log
    services = patientLogFile.inclusive_service.all()
    prescriptions = patientLogFile.prescription.all()
    facility = Facility.objects.all()[0]
    # totalservices=(prescriptions.count()) + services.count()
    allItems = []
    for p in prescriptions:
        allItems.append(p)
    for s in services:
        allItems.append(s)
    t = 0
    cumulative_totals=[]
    for item in allItems:
        t += item.total_amount
        cumulative_totals.append(t)
    # totalservices=(prescriptions.count()) + services.count()
    page_title = 'Invoice for '+patientLogFile.patient.full_name()
    context = {'page_title':page_title,'paymentlog':paymentLogFile,'allItems':allItems,'hide_skeleton':True,'cumulative_totals':cumulative_totals,'cur_date':datetime.date.today(),'facility':facility}
    return render(request,'base/cashier/invoice-print.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashierReceipt(request,pk):
    paymentLogFile = DebitPaymentLog.objects.get(id=pk)
    patientLogFile = paymentLogFile.pat_log
    services = patientLogFile.inclusive_service.all()
    prescriptions = patientLogFile.prescription.all()
    # totalservices=(prescriptions.count()) + services.count()
    allItems = []
    for p in prescriptions:
        allItems.append(p)
    for s in services:
        allItems.append(s)
    t = 0
    cumulative_totals=[]
    for item in allItems:
        t += item.total_amount
        cumulative_totals.append(t)
    # totalservices=(prescriptions.count()) + services.count()
    page_title = 'Cash Receipt for '+patientLogFile.patient.full_name()
    context = {'page_title':page_title,'paymentlog':paymentLogFile,'allItems':allItems,'hide_skeleton':True,'cumulative_totals':cumulative_totals}
    return render(request,'base/cashier/cash-receipt.html',context)

@login_required(login_url="login")
@permission_required(user_perms('cashier'),login_url='no-permission')
def cashFinalize(request,pk):
    patientLogFile = PatientLog.objects.get(id=pk)
    services = patientLogFile.inclusive_service.all()
    prescriptions = patientLogFile.prescription.all()
    totalPrice = 0
    if (patientLogFile.payment_mode.payer_class.mode_class).lower() == 'invoice':        
        form = DebitPayLogFormInv()
    else:
        form = DebitPayLogForm()
    for p in prescriptions:
        totalPrice+=(p.price*p.quantity)
    for s in services:
        totalPrice+=(s.price*s.quantity)
    if(request.method == 'POST'):
        if (patientLogFile.payment_mode.payer_class.mode_class).lower() == 'invoice':
            form = DebitPayLogFormInv(request.POST)
        else:
            form = DebitPayLogForm(request.POST)
        if form.is_valid():
            payfile=form.save(commit=False)
            payfile.dpy_id=createId(DebitPaymentLog,DebitPaymentLog.dpy_id,'DPY')
            payfile.pat_log=patientLogFile
            payfile.balance=payfile.calc_bal()
            payfile.added_by=request.user
            payfile.save()
            if payfile.balance==0:
                patientLogFile.cash_cleared=True
            patientLogFile.med_cleared=True
            patientLogFile.active_status=False
            patientLogFile.total_charge=totalPrice
            patientLogFile.save()
            for p in prescriptions:
                p.paid=True
                p.save()
            for s in services:
                s.paid = True
                s.save()
            messages.success(request,'Finalized Successfully.')
            return redirect('cash-receipt',payfile.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Finalize Payment'
    context = {'page_title':page_title,'patientlog':patientLogFile,'form':form,'hide_skeleton':True,'billable_amount':totalPrice}
    return render(request,'base/cashier/finalize-payment.html',context)

#med and its related files
@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def med(request):
    page_title = 'Med & Consultation Office'
    context = {'page_title':page_title}
    return render(request,'base/med/med.html',context)

@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def medUncompleted(request):
    if Department.objects.filter(role='consultation').exists():
        docDptid = Department.objects.get(role='consultation').id
    patientLogFiles = []
    for patlog in PatientLog.objects.filter(active_status=True,current_stage=docDptid).order_by('-emergency_code__id','-patlog_id'):        
        if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Med Uncompleted'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/med/uncompleted.html',context)

@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def medInpatients(request):
    if Department.objects.filter(role='consultation').exists():
        docDptid = Department.objects.get(role='consultation').id
    inpatientlogs = []
    for patlog in Inpatient.objects.filter(patient_file__active_status=True,patient_file__admission_category='INPATIENT'):
        inpatientlogs.append(patlog)
    page_title = 'Med Inpatients'
    context = {'page_title':page_title,'inpatientlogs':inpatientlogs}
    return render(request,'base/med/inpatients.html',context)

@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def medEditPrescriptions(request,pk):
    drugs = Drug.objects.all()
    patientLogFile = PatientLog.objects.get(id=pk)
    prescriptions = patientLogFile.prescription.all()
    form = PrescriptionForm()
    if(request.method == 'POST'):
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prcfile=form.save(commit=False)
            prcfile.prcp_id=createId(Prescription,Prescription.prcp_id,'PRC')
            prcfile.patient=patientLogFile.patient
            prcfile.patlog=patientLogFile
            prcfile.user=request.user
            prcfile.save()
            prcfile.total_amount = prcfile.get_total_price()
            prcfile.save()
            patientLogFile.prescription.add(prcfile)
            drugrec = Drug.objects.get(id=prcfile.drug.id)
            drugrec.quantity -= prcfile.quantity
            drugrec.save()
            messages.success(request,str(drugrec)+' has been updated successfully!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Edit Prescription'
    context = {'page_title':page_title,'patientlog':patientLogFile,'form':form,'drugs':drugs,'hide_skeleton':True,'prescriptions':prescriptions}
    return render(request,'base/med/create-prescription.html',context)

@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def delPrescriptions(request,pk):
    if Prescription.objects.filter(id=pk).exists():
        prescription = Prescription.objects.get(id=pk)
        drugrec = Drug.objects.get(id=prescription.drug.id)
        drugrec.quantity += prescription.quantity
        drugrec.save()
        prescription.delete()
        messages.success(request,str(drugrec)+" has been removed successfully.")
    else:
        messages.error(request,"Prescription record does not exist.")
    return redirect(request.META['HTTP_REFERER'])
    
@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def delService(request,pk):
    if ServiceLog.objects.filter(id=pk).exists():
        srvfile = ServiceLog.objects.get(id=pk)
        srvfile.delete()
        messages.success(request,str(srvfile)+" has been removed successfully.")
    else:
        messages.error(request,"Service record does not exist.")
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def medEditServices(request,pk):
    services = Service.objects.all()
    patientLogFile = PatientLog.objects.get(id=pk)
    ser_logs = patientLogFile.inclusive_service.all()
    form = ServiceLogForm()
    if(request.method == 'POST'):
        form = ServiceLogForm(request.POST)
        if form.is_valid():
            srvfile=form.save(commit=False)
            srvfile.sl_id=createId(ServiceLog,ServiceLog.sl_id,'SRL')
            srvfile.patient=patientLogFile.patient
            srvfile.patient_log=patientLogFile
            srvfile.user=request.user
            srvfile.save()
            srvfile.total_amount = srvfile.get_total_price()
            srvfile.save()
            patientLogFile.inclusive_service.add(srvfile)
            messages.success(request,str(srvfile)+' has been added successfully!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Edit Service'
    context = {'page_title':page_title,'patientlog':patientLogFile,'form':form,'services':services,'hide_skeleton':True,'ser_logs':ser_logs}
    return render(request,'base/med/create-service.html',context)

@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def medCompleted(request):
    if Department.objects.filter(role='consultation').exists():
        docDptid = Department.objects.get(role='consultation').id
    patientLogFiles = []
    for patlog in PatientLog.objects.filter(med_cleared=True).order_by('-patlog_id'):
        if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Med Completed'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/med/completed.html',context)

@login_required(login_url="login")
@permission_required(user_perms('doctor'),login_url='no-permission')
def medPatientFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    drugs = Drug.objects.all()
    patientLogFile = PatientLog.objects.get(id=pk)
    prev_files =[]
    for file in PatientLog.objects.filter(patient=patientLogFile.patient,active_status=False):
        if not file==patientLogFile:
            prev_files.append(file)
    services = patientLogFile.inclusive_service.all()
    prescriptions = patientLogFile.prescription.all()
    form = PatientLogForm(instance=patientLogFile)
    if(request.method == 'POST'):
        form = PatientLogForm(request.POST,instance=patientLogFile)
        if form.is_valid():
            logfile=form.save(commit=False)
            logfile.med_cleared = True
            logfile.save()
            logfile.involved_depts.add(request.POST.get('current_stage'))
            messages.success(request,'Patient data saved successfully!')
            return redirect('med-uncompleted')
        else:
            messages.error(request,form.errors)
    page_title = 'Med Patient File'
    context = {'page_title':page_title,'form':form,'patientlog':patientLogFile,'services':services,'departments':departments,'drugs':drugs,'prescriptions':prescriptions,'prev_files':prev_files}
    return render(request,'base/med/patient-file.html',context)
#end of med

#start of nursing and related files
@login_required(login_url="login")
@permission_required(user_perms('nurse'),login_url='no-permission')
def nurse(request):
    page_title = 'Nurse Office'
    context = {'page_title':page_title}
    return render(request,'base/nurse/nurse.html',context)

@login_required(login_url="login")
@permission_required(user_perms('nurse'),login_url='no-permission')
def nurseUncompleted(request):
    if Department.objects.filter(role='nursing').exists():
        nurDptid = Department.objects.get(role='nursing').id
    patientLogFiles = []
    for patlog in PatientLog.objects.filter(active_status=True,med_cleared=False,current_stage=nurDptid):        
        if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Nurse | Uncompleted'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/nurse/unattended.html',context)

@login_required(login_url="login")
@permission_required(user_perms('nurse'),login_url='no-permission')
def nurseInpatients(request):
    patientLogFiles = []
    for patlog in Inpatient.objects.filter(patient_file__active_status=True,patient_file__admission_category='INPATIENT'):
        patientLogFiles.append(patlog)
    page_title = 'Nurse | Inpatients'
    context = {'page_title':page_title,'inpatientlogs':patientLogFiles}
    return render(request,'base/nurse/inpatients.html',context)

@login_required(login_url="login")
@permission_required(user_perms('nurse'),login_url='no-permission')
def nursePatientFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    services = Service.objects.all()
    patientLogFile = PatientLog.objects.get(id=pk)
    form = NursePatientLogForm(instance=patientLogFile)
    if(request.method == 'POST'):
        form = NursePatientLogForm(request.POST,instance=patientLogFile)
        if form.is_valid():
            logfile=form.save(commit=False)
            logfile.save()
            logfile.involved_depts.add(request.POST.get('current_stage'))
            messages.success(request,'Patient data saved successfully!')
            return redirect('nurse-unattended')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Nurse | View Patient File'
    context = {'page_title':page_title,'form':form,'patientlog':patientLogFile,'services':services,'departments':departments}
    return render(request,'base/nurse/patient-file.html',context)\
        
@login_required(login_url="login")
@permission_required(user_perms('nurse'),login_url='no-permission')
def nurseInpatientFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    services = Service.objects.all()
    inpatientFile = Inpatient.objects.get(id=pk)
    form = InpatientForm(instance=inpatientFile)
    if(request.method == 'POST'):
        form = InpatientForm(request.POST,instance=inpatientFile)
        if form.is_valid():
            logfile=form.save(commit=False)
            logfile.save()
            # logfile.involved_depts.add(request.POST.get('current_stage'))
            messages.success(request,'Patient data saved successfully!')
            return redirect('nurse-inpatients')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Nurse | View Patient File'
    context = {'page_title':page_title,'form':form,'inpatientFile':inpatientFile,'services':services,'departments':departments}
    return render(request,'base/nurse/inpatient-file.html',context)
#end of nurse
# pharmacy and its related files
@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacy(request):
    page_title = 'Pharmacy Office'
    context = {'page_title':page_title}
    return render(request,'base/pharmacy/pharmacy.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyUncompleted(request):
    if Department.objects.filter(role='pharmacy').exists():
        pharDptid = Department.objects.get(role='pharmacy').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(active_status=True,current_stage=pharDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Pharmacy | View Uncompleted Records'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/pharmacy/uncompleted.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyCompleted(request):
    if Department.objects.filter(role='pharmacy').exists():
        pharDptid = Department.objects.get(role='pharmacy').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(involved_depts=pharDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Pharmacy | View Completed Records'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/pharmacy/completed.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyPatFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    patientLogFile = PatientLog.objects.get(id=pk)
    # services = patientLogFile.inclusive_service.all()
    prescriptions = patientLogFile.prescription.all()
    form = PharPatientLogForm(instance=patientLogFile)
    if(request.method == 'POST'):
        form = PharPatientLogForm(request.POST,instance=patientLogFile)
        if form.is_valid():
            patform=form.save(commit=False)
            patform.pharmacy_cleared=True
            patform.save()
            patform.involved_depts.add(request.POST.get('current_stage'))
            messages.success(request,'Patient data updated successfully!')
            return redirect('pharmacy-uncompleted')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Pharmacy | View Patient File'
    context = {'page_title':page_title,'patientlog':patientLogFile,'departments':departments,'prescriptions':prescriptions}
    return render(request,'base/pharmacy/patient-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyAddDrug(request):
    drugs_inventory = Drug.objects.all()
    form = PharNewDrugForm()
    if(request.method == 'POST'):
        form = PharNewDrugForm(request.POST)
        if form.is_valid():
            drug_name = request.POST.get('drug_name')
            drugform=form.save(commit=False)
            drugform.drugId=createId(Drug,Drug.drugId,'DRU')
            drugform.added_by=request.user
            drugform.save()
            messages.success(request,str(drug_name)+' saved successfully!')
            return redirect('pharmacy-new-drug')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Pharmacy | Add New Drug'
    context = {'page_title':page_title,'drugs_inventory':drugs_inventory,'form':form}
    return render(request,'base/pharmacy/new-drug.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyStocksPage(request):
    drugs_inventory = Drug.objects.all()
    page_title = 'Pharmacy | Stock Records'
    context = {'page_title':page_title,'drugs_inventory':drugs_inventory}
    return render(request,'base/pharmacy/stock-records.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyStocksAdjustmentListing(request):
    drugs_inventory = Drug.objects.all()
    page_title = 'Pharmacy | Stocks Adjustment Listing'
    context = {'page_title':page_title,'drugs_inventory':drugs_inventory}
    return render(request,'base/pharmacy/stock-adjustment.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyDrugsInventory(request):
    drugs_inventory = Drug.objects.all()
    page_title = 'Pharmacy | Drugs Inventory'
    context = {'page_title':page_title,'drugs_inventory':drugs_inventory}
    return render(request,'base/pharmacy/drugs-inventory.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyAdjustDrug(request,pk):
    drug_obj = Drug.objects.get(id=pk)
    form = PharDrugAdjustForm(instance=drug_obj)
    if(request.method == 'POST'):
        form = PharDrugAdjustForm(request.POST,instance=drug_obj)
        if form.is_valid():
            drug_name = request.POST.get('drug_name')
            form.save()
            messages.success(request,str(drug_name)+' changed successfully!')
            return redirect('pharmacy-adjustment-listing')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Pharmacy | Adjust Drug Details'
    context = {'page_title':page_title,'drug_obj':drug_obj,'form':form}
    return render(request,'base/pharmacy/adjust-drug.html',context)

@login_required(login_url="login")
@permission_required(user_perms('pharmacy'),login_url='no-permission')
def pharmacyStockTake(request):
    drugs_inventory = Drug.objects.all()
    form = StockTakeForm()
    current_date = timezone.localdate()
    records_created_today = []
    for stockTakeRec in DrugStockTake.objects.filter(created__date=current_date):
        if stockTakeRec.created_today():
            records_created_today.append(stockTakeRec)
    if request.method == 'POST':
        form = StockTakeForm(request.POST)
        if form.is_valid():
            st_file=form.save(commit=False)
            st_file.recId = createId(DrugStockTake,DrugStockTake.recId,'DST')
            st_file.added_by=request.user
            st_file.save()
            new_drug_count = st_file.new_quantity+st_file.existing_quantity
            st_file.drug.quantity=new_drug_count
            st_file.drug.save()
            messages.success(request,'Stock Take record submitted successfully!😉')
            return redirect('pharmacy-stock-take')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Stock Take'
    context = {'page_title':page_title,'all_drugs':drugs_inventory,'form':form,'records_created_today':records_created_today}
    return render(request,'base/pharmacy/stock-take-form.html',context)
#end of pharmacy

# start of hr and related files
@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def humanResource(request):
    page_title = 'Human Resource Office'
    context = {'page_title':page_title}
    return render(request,'base/human-resource/human-resource.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrManageEmployees(request):
    page_title = 'HR | Manage Employees'
    form = EmployeeForm()
    context = {'page_title':page_title,'form':form}
    return render(request,'base/human-resource/manage-employees.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrNewEmployee(request):
    page_title = 'Add New Employee'
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employeeform=form.save(commit=False)
            employeeform.employee_id=createId(Employee,Employee.employee_id,'EML')
            employeeform.save()
            messages.success(request,str(employeeform)+' has been reqistered successfully.')
            return redirect('hr-manage-employees')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    context = {'page_title':page_title,'form':form}
    return render(request,'base/human-resource/new-employee.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrEmployeeEvaluation(request):
    page_title = 'Employee Evaluation'
    context = {'page_title':page_title}
    return render(request,'base/human-resource/employee-evaluation.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrEmployeeEvaluationList(request):
    page_title = 'Employee List For Evaluation'
    all_employees = Employee.objects.all()
    context = {'page_title':page_title,'all_employees':all_employees}
    return render(request,'base/human-resource/employee-evaluation-list.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrCompletedEvaluations(request):
    page_title = 'Employee List For Evaluation'
    all_evaluations = EmployeeEvaluation.objects.all()
    context = {'page_title':page_title,'all_evaluations':all_evaluations}
    return render(request,'base/human-resource/completed-evaluations.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrEmployeeEvaluationFile(request,pk):
    page_title = 'Employee Evaluation'
    employee = Employee.objects.get(id=pk)
    form = EmployeeEvaluationForm()
    if request.method == 'POST':
        form = EmployeeEvaluationForm(request.POST)
        if form.is_valid():
            employeeform=form.save(commit=False)
            employeeform.employee_id=createId(EmployeeEvaluation,EmployeeEvaluation.evl_id,'EVF')
            employeeform.employee = employee
            employeeform.user = request.user
            employeeform.save()
            messages.success(request,'Evaluation for '+str(employeeform)+' has been completed successfully.')
            return redirect('hr-evaluation')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    context = {'page_title':page_title,'form':form,'employee':employee}
    return render(request,'base/human-resource/new-evaluation-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrOpenEvaluationFile(request,pk):
    page_title = 'Employee Evaluation'
    evaluationFile = EmployeeEvaluation.objects.get(id=pk)
    attendances = evaluationFile.attendance_logs.all()
    previous_leaves = evaluationFile.leaves_taken.all()
    form = EmployeeEvaluationForm(instance=evaluationFile)
    if request.method == 'POST':
        form = EmployeeEvaluationForm(request.POST,instance=evaluationFile)
        if form.is_valid():
            employeeform=form.save(commit=False)
            employeeform.user = request.user
            employeeform.save()
            messages.success(request,'Evaluation for '+str(employeeform)+' has been changed successfully.')
            return redirect('hr-completed-evaluations')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    context = {'page_title':page_title,'form':form,'evaluationFile':evaluationFile,'attendances':attendances,'previous_leaves':previous_leaves}
    return render(request,'base/human-resource/open-evaluation-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrEmployeeTermination(request):
    page_title = 'Human Resource Office'
    context = {'page_title':page_title}
    return render(request,'base/human-resource/employee-termination.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrEmployeeList(request):
    all_employees=Employee.objects.all()
    page_title = 'HR | All Employees'
    context = {'page_title':page_title,'all_employees':all_employees}
    return render(request,'base/human-resource/employee-list.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrEmployeeFile(request,pk):
    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(instance=employee)
    departments = Department.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(request.POST,instance=employee)
        if form.is_valid():
            employeeform=form.save()
            messages.success(request,str(employeeform)+' file has been updated successfully.')
            return redirect('hr-manage-employees')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'HR | File For ' + str(employee)
    context = {'page_title':page_title,'employee':employee,'form':form,'departments':departments}
    return render(request,'base/human-resource/employee-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrLeaveMgm(request):
    page_title = 'HR | Employee Leave Management'
    context = {'page_title':page_title}
    return render(request,'base/human-resource/leave-mgm.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrLeaveRequests(request,pk):
    pk=int(pk)
    if pk == 0:
        leave_requests = EmployeeLeave.objects.all()
        rq_filter = 'All'
    else:
        leave_requests = EmployeeLeave.objects.filter(status__status_code=pk)
        leave_status = LeaveStatus.objects.get(status_code=pk)
        rq_filter = str(leave_status.status_description)
    page_title = rq_filter+' Leave Requests'
    context = {'page_title':page_title,'leave_requests':leave_requests}
    return render(request,'base/human-resource/leave-requests.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrLeaveRequestFile(request,pk):
    leave_file = EmployeeLeave.objects.get(id=pk)
    form = EmployeeLeaveApprovalForm(instance=leave_file)
    leave_stats = LeaveStatus.objects.all()
    if request.method == 'POST':
        form = EmployeeLeaveApprovalForm(request.POST,instance=leave_file)
        if form.is_valid():
            form.save()
            messages.success(request,"Leave Details updated Successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Leave Details'
    context = {'page_title':page_title,'leave_file':leave_file,'form':form,'leave_stats':leave_stats}
    return render(request,'base/human-resource/leave-request-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrAddLeave(request):
    form = EmployeeLeaveApplicationForm()
    leave_stats = LeaveStatus.objects.all()
    if request.method == 'POST':
        form = EmployeeLeaveApplicationForm(request.POST)
        if form.is_valid():
            cur_status = LeaveStatus.objects.get(id=1)
            leave_form=form.save(commit=False)
            leave_form.leave_id=createId(EmployeeLeave,EmployeeLeave.leave_id,'ELV')
            leave_form.user=request.user
            leave_form.status=cur_status
            leave_form.save()
            messages.success(request,"Leave Details updated Successfully.")
            return redirect('hr-leave-mgm')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Leave Details'
    context = {'page_title':page_title,'form':form,'leave_stats':leave_stats}
    return render(request,'base/human-resource/add-leave.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrPayroll(request):
    page_title = 'Payroll Manager'
    context = {'page_title':page_title}
    return render(request,'base/human-resource/payroll.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrAddPayroll(request):
    page_title = 'Add New Transactions'
    form = PayrollForm()
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            pay_form=form.save(commit=False)
            pay_form.rec_id=createId(Payroll,Payroll.rec_id,'PTR')
            pay_form.user=request.user
            pay_form.cleared=True
            pay_form.save()
            messages.success(request,"Payroll data updated Successfully.")
            return redirect('hr-payroll')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    
    context = {'page_title':page_title,'form':form}
    return render(request,'base/human-resource/payment-form.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrPayrollRecs(request,pk):
    pk=int(pk)
    if pk == 0:
        payroll_records = Payroll.objects.all()
        rq_filter = 'All'
    elif pk == 1:
        current_date = timezone.localdate()
        payroll_records = Payroll.objects.filter(created__date=current_date,cleared=True)
        rq_filter = 'Today\'s'
    elif pk == 2:
        payroll_records = Payroll.objects.filter(cleared=False)
        rq_filter = 'Pending'
    else:
        payroll_records = Payroll.objects.all()
        rq_filter = 'All'
    page_title = rq_filter+' Payment Records'
    context = {'page_title':page_title,'payroll_records':payroll_records}
    return render(request,'base/human-resource/payroll-records.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrPayrollRecordFile(request,pk):
    payroll_record_file = Payroll.objects.get(id=pk)
    if request.method == 'POST':
        form = PayrollApprovalForm(request.POST,instance=payroll_record_file)
        if form.is_valid():
            form.save()
            messages.success(request,"Leave Details updated Successfully.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Leave Details'
    context = {'page_title':page_title,'payroll_record_file':payroll_record_file}
    return render(request,'base/human-resource/payroll-record-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrAttendance(request):
    page_title = 'Human Resource Office'
    context = {'page_title':page_title}
    return render(request,'base/human-resource/attendance.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrAttendanceNew(request):
    page_title = 'Attendance Form'
    form = EmployeeAttendanceForm()
    if request.method == 'POST':
        form = EmployeeAttendanceForm(request.POST)
        if form.is_valid():
            att_form=form.save(commit=False)
            att_form.rec_id=createId(AttendanceLog,AttendanceLog.rec_id,'REC')
            att_form.user = request.user
            att_form.save()
            messages.success(request,str(att_form)+" has been checked in successfully 👍.")
            return redirect('hr-attendance')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    context = {'page_title':page_title,'form':form}
    return render(request,'base/human-resource/attendance-new.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrAttendanceFile(request,pk):
    attendance_file = AttendanceLog.objects.get(id=pk)
    page_title = 'Attendance Form'
    form = EmployeeCheckoutForm(instance=attendance_file)
    if request.method == 'POST':
        form = EmployeeCheckoutForm(request.POST,instance=attendance_file)
        if form.is_valid():
            att_form=form.save(commit=False)
            att_form.user = request.user
            att_form.save()
            messages.success(request,str(att_form)+" has been checked out successfully 👍.")
            return redirect('hr-attendance')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    context = {'page_title':page_title,'form':form,'attendance_file':attendance_file}
    return render(request,'base/human-resource/attendance-file.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrAttendanceDaily(request):
    page_title = 'HR | Daily Attendance List'
    current_date = timezone.localdate()
    all_records = AttendanceLog.objects.filter(created__date=current_date)[0:100]
    context = {'page_title':page_title,'all_records':all_records}
    return render(request,'base/human-resource/attendance-list.html',context)

@login_required(login_url="login")
@permission_required(user_perms('hr'),login_url='no-permission')
def hrAttendanceAll(request):
    all_records = AttendanceLog.objects.all()[0:100]
    page_title = 'HR | Attendance List'
    context = {'page_title':page_title,'all_records':all_records}
    return render(request,'base/human-resource/attendance-list.html',context)

#end of hr

@login_required(login_url="login")
@permission_required(user_perms('finance'),login_url='no-permission')
def finance(request):
    page_title = 'Finance Office'
    context = {'page_title':page_title}
    return render(request,'base/finance/finance.html',context)

@login_required(login_url="login")
@permission_required(user_perms('finance'),login_url='no-permission')
def finance_dpt_collections(request):
    dpt_collections = {}
    for dpt in Department.objects.filter(handles_patient=True):
        if not dpt.role in dpt_collections:
            if not dpt.handles_drugs:
                dpt_collections[str(dpt.role)]=daily_departmental_income(dpt)
            else:
                dpt_collections[str(dpt.role)]=daily_pharmacy_income()
    page_title = 'Departmental Collections'
    context = {'page_title':page_title,'collections':dpt_collections}
    return render(request,'base/finance/dept-collections.html',context)

@login_required(login_url="login")
@permission_required(user_perms('finance'),login_url='no-permission')
def financeDailyCollection(request):
    total_amount=[0,0,0]
    total_cash = [0,0,0]
    total_epay = [0,0,0]
    total_receipts = [0,0,0]
    total_inv = [0,0,0]
    pharmacy_amount = [0,0,0]
    # these dictionaries contain data in this  format: {'name':[outpatient_total,inpatient_total,grand_total]}
    payers_list={}
    cash_opt_list={}
    departments_list={}
    paymode_list={}
    departments = Department.objects.filter(handles_patient=True)
    cash_options = CashOption.objects.all()
    insurances = PayerScheme.objects.filter(payer_class__mode_name='Invoice')
    current_date=timezone.localdate()
    all_records = DebitPaymentLog.objects.filter(created__date=current_date)
    #getting all services/prescriptions associated with the listed payments
    service_logs = []
    prescriptions = []
    for rec in all_records:
        # payer += r.payer
        if (rec.pat_log.patient.admission_category).lower()=='op':
            total_amount[0] += rec.billable_amount
            total_amount[2] += rec.billable_amount
            total_cash[0] += rec.cash_value
            total_cash[2] += rec.cash_value
            total_receipts[0] += rec.cash_value
            total_receipts[2] += rec.cash_value
            total_epay[0] += rec.epay_value
            total_epay[2] += rec.epay_value
            total_receipts[0] += rec.epay_value
            total_receipts[2] += rec.epay_value
            total_inv[0] += rec.invoice_value
            total_inv[2] += rec.invoice_value
            
        else:
            total_amount[1] += rec.billable_amount
            total_amount[2] += rec.billable_amount
            total_cash[1] += rec.cash_value
            total_cash[2] += rec.cash_value
            total_receipts[1] += rec.cash_value
            total_receipts[2] += rec.cash_value
            total_epay[1] += rec.epay_value
            total_epay[2] += rec.epay_value
            total_receipts[1] += rec.epay_value
            total_receipts[2] += rec.epay_value
            total_inv[1] += rec.invoice_value
            total_inv[2] += rec.invoice_value
        for s in ServiceLog.objects.filter(patient_log=rec.pat_log):
            service_logs.append(s)
        for p in Prescription.objects.filter(patlog=rec.pat_log):
            prescriptions.append(p)
        #geting all transactions that are paid through all payment modes with their totals
        for i in PaymentMode.objects.all():
            # for rec in all_records:
                if rec.payer.payer_class == i:
                    if not str(rec.payer.payer_class) in paymode_list:
                        if (rec.pat_log.patient.admission_category).lower()=='op':
                            paymode_list[str(rec.payer.payer_class)]=[rec.billable_amount,0,rec.billable_amount]
                        else:
                            paymode_list[str(rec.payer.payer_class)]=[rec.billable_amount,rec.billable_amount,0]
                    else:
                        if (rec.pat_log.patient.admission_category).lower()=='op':
                            paymode_list[str(rec.payer.payer_class)][0]+=rec.billable_amount
                            paymode_list[str(rec.payer.payer_class)][2]+=rec.billable_amount
                            
                        else:
                            paymode_list[str(rec.payer.payer_class)][1]+=rec.billable_amount
                            paymode_list[str(rec.payer.payer_class)][2]+=rec.billable_amount
        #geting all transactions that are paid through invoice with their totals
        for i in insurances:
            # for rec in all_records:
                if rec.payer == i:
                    if not str(rec.payer) in payers_list:
                        if (rec.pat_log.patient.admission_category).lower()=='op':
                            payers_list[str(rec.payer)]=[rec.billable_amount,0,rec.billable_amount]
                        else:
                            payers_list[str(rec.payer)]=[rec.billable_amount,rec.billable_amount,0]
                    else:
                        if (rec.pat_log.patient.admission_category).lower()=='op':
                            payers_list[str(rec.payer)][0]+=rec.billable_amount
                            payers_list[str(rec.payer)][2]+=rec.billable_amount
                            
                        else:
                            payers_list[str(rec.payer)][1]+=rec.billable_amount
                            payers_list[str(rec.payer)][2]+=rec.billable_amount
        #geting all transactions that are paid through cash/epay with their totals
        for c in cash_options:
            # for rec in all_records:
                if rec.cash_option == c:
                    if not str(rec.cash_option) in cash_opt_list:
                        if (rec.pat_log.patient.admission_category).lower()=='op':
                            cash_opt_list[str(rec.cash_option)]=[rec.billable_amount,0,rec.billable_amount]
                        else:
                            cash_opt_list[str(rec.cash_option)]=[rec.billable_amount,rec.billable_amount,0]
                    else:
                        if (rec.pat_log.patient.admission_category).lower()=='op':
                            cash_opt_list[str(rec.cash_option)][0]+=rec.billable_amount
                            cash_opt_list[str(rec.cash_option)][2]+=rec.billable_amount
                            
                        else:
                            cash_opt_list[str(rec.cash_option)][1]+=rec.billable_amount
                            cash_opt_list[str(rec.cash_option)][2]+=rec.billable_amount
    #geting total service and procedure income from departments
    for s in service_logs:
        for dpt in departments:
            if s.service.department == dpt:
                if not str(s.service.department) in departments_list:
                    if (s.patient.admission_category).lower()=='op':
                        departments_list[str(s.service.department)]=[s.total_amount,0,s.total_amount]
                    else:
                        departments_list[str(s.service.department)]=[s.total_amount,s.total_amount,0]
                else:
                    if (s.patient.admission_category).lower()=='op':
                        departments_list[str(s.service.department)][0]+=s.total_amount
                        departments_list[str(s.service.department)][2]+=s.total_amount
                        
                    else:
                        departments_list[str(s.service.department)][1]+=s.total_amount
                        departments_list[str(s.service.department)][2]+=s.total_amount
    #geting total from drugs income
    for p in prescriptions:
        if (p.patient.admission_category).lower()=='op':
            pharmacy_amount[0]+=p.total_amount
            pharmacy_amount[2]+=p.total_amount
            
        else:
            pharmacy_amount[1]+=p.total_amount
            pharmacy_amount[2]+=p.total_amount
        # pharmacy_amount+=p.total_amount
                    
    totals_list = {'total_cash':total_cash,'total_inv':total_inv,'total_epay':total_epay,'total_amount':total_amount,'total_receipts':total_receipts}
    page_title = 'Daily Collection Report'
    context = {'page_title':page_title,'payment_modes':paymode_list,'departments':departments_list,'cash_options':cash_opt_list,'insurances':payers_list,'all_records':all_records,'totals_list':totals_list,'pharmacy_amount':pharmacy_amount,'hide_skeleton':True}
    return render(request,'base/finance/collection-report.html',context)

#imaging and radiography with its related fields
@login_required(login_url="login")
@permission_required(user_perms('imaging'),login_url='no-permission')
def imaging_and_radiography(request):
    page_title = 'Imaging And Radiography Office'
    context = {'page_title':page_title}
    return render(request,'base/imaging/imaging.html',context)

@login_required(login_url="login")
@permission_required(user_perms('imaging'),login_url='no-permission')
def imagingUncompleted(request):
    if Department.objects.filter(role='imaging').exists():
        invDptid = Department.objects.get(role='imaging').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(active_status=True,current_stage=invDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Uncompleted Patient Files'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/imaging/uncompleted.html',context)

@login_required(login_url="login")
@permission_required(user_perms('imaging'),login_url='no-permission')
def imagingCompleted(request):
    if Department.objects.filter(role='imaging').exists():
        invDptid = Department.objects.get(role='imaging').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(involved_depts=invDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Completed Patient Files'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/imaging/completed.html',context)

@login_required(login_url="login")
@permission_required(user_perms('imaging'),login_url='no-permission')
def imagingPatFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    if Department.objects.filter(role='imaging').exists():
        invDptid = Department.objects.get(role='imaging').id
    patientLogFile = PatientLog.objects.get(id=pk)
    # services = patientLogFile.inclusive_service.all()
    tests = patientLogFile.inclusive_service.filter(service__department=invDptid)
    form = ImagingPatientLogForm(instance=patientLogFile)
    if(request.method == 'POST'):
        form = ImagingPatientLogForm(request.POST,instance=patientLogFile)
        if form.is_valid():
            patform=form.save(commit=False)
            patform.save()
            patform.involved_depts.add(request.POST.get('current_stage'))
            for test in tests:
                ImagingLog.objects.create(
                    rec_id = createId(ImagingLog,ImagingLog.rec_id,'TST'),
                    service_log = test,
                    quantity = test.quantity,
                    pat_log = patform,
                    results = patform.test_results,
                    cleared = True
                )
            messages.success(request,'Patient data updated successfully!')
            return redirect('imaging-uncompleted')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

    page_title = 'Imaging | Patient File'
    context = {'page_title':page_title,'patientlog':patientLogFile,'departments':departments,'tests':tests}
    return render(request,'base/imaging/patient-file.html',context)

#dental department with its related fields
@login_required(login_url="login")
@permission_required(user_perms('dental'),login_url='no-permission')
def dental(request):
    page_title = 'Dental Department'
    context = {'page_title':page_title}
    return render(request,'base/dental/dental.html',context)

@login_required(login_url="login")
@permission_required(user_perms('dental'),login_url='no-permission')
def dentalUncompleted(request):
    if Department.objects.filter(role='dental').exists():
        invDptid = Department.objects.get(role='dental').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(active_status=True,current_stage=invDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Uncompleted Patient Files'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/dental/uncompleted.html',context)

@login_required(login_url="login")
@permission_required(user_perms('dental'),login_url='no-permission')
def dentalCompleted(request):
    if Department.objects.filter(role='dental').exists():
        invDptid = Department.objects.get(role='dental').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(involved_depts=invDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Completed Patient Files'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/dental/completed.html',context)

@login_required(login_url="login")
@permission_required(user_perms('dental'),login_url='no-permission')
def dentalPatFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    if Department.objects.filter(role='dental').exists():
        invDptid = Department.objects.get(role='dental').id
    patientLogFile = PatientLog.objects.get(id=pk)
    procedures = patientLogFile.inclusive_service.filter(service__department=invDptid)
    prescriptions = patientLogFile.prescription.all()
    form = DentalPatientLogForm(instance=patientLogFile)
    if(request.method == 'POST'):
        form = DentalPatientLogForm(request.POST,instance=patientLogFile)
        if form.is_valid():
            patform=form.save(commit=False)
            patform.save()
            patform.involved_depts.add(request.POST.get('current_stage'))
            for proc in procedures:
                DentalLog.objects.create(
                    rec_id = createId(DentalLog,DentalLog.rec_id,'PRC'),
                    service_log = proc,
                    quantity = proc.quantity,
                    pat_log = patform,
                    results = patform.test_results,
                    cleared = True
                )
            messages.success(request,'Patient data updated successfully!')
            return redirect('dental-uncompleted')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

    page_title = 'Dental | Patient File'
    context = {'page_title':page_title,'patientlog':patientLogFile,'departments':departments,'procedures':procedures,'prescriptions':prescriptions}
    return render(request,'base/dental/patient-file.html',context)

# lab & investigations
@login_required(login_url="login")
@permission_required(user_perms('lab'),login_url='no-permission')
def investigations(request):
    page_title = 'Lab & Investigations Office'
    context = {'page_title':page_title}
    return render(request,'base/investigations/investigations.html',context)

@login_required(login_url="login")
@permission_required(user_perms('lab'),login_url='no-permission')
def investigationsUncompleted(request):
    if Department.objects.filter(role='laboratory').exists():
        invDptid = Department.objects.get(role='laboratory').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(active_status=True,current_stage=invDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Uncompleted Patient Files'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/investigations/uncompleted.html',context)

@login_required(login_url="login")
@permission_required(user_perms('lab'),login_url='no-permission')
def investigationsCompleted(request):
    if Department.objects.filter(role='laboratory').exists():
        invDptid = Department.objects.get(role='laboratory').id
    patientLogFiles = []
    current_date = timezone.localdate()
    for patlog in PatientLog.objects.filter(involved_depts=invDptid,created__date=current_date):        
        # if patlog.created_today():
            patientLogFiles.append(patlog)
    page_title = 'Completed Patient Files'
    context = {'page_title':page_title,'patientlogs':patientLogFiles}
    return render(request,'base/investigations/completed.html',context)

@login_required(login_url="login")
@permission_required(user_perms('lab'),login_url='no-permission')
def investigationsPatFile(request,pk):
    departments = Department.objects.filter(handles_patient=True)
    if Department.objects.filter(role='laboratory').exists():
        invDptid = Department.objects.get(role='laboratory').id
    patientLogFile = PatientLog.objects.get(id=pk)
    # services = patientLogFile.inclusive_service.all()
    tests = patientLogFile.inclusive_service.filter(service__department=invDptid)
    form = LabPatientLogForm(instance=patientLogFile)
    if(request.method == 'POST'):
        form = LabPatientLogForm(request.POST,instance=patientLogFile)
        if form.is_valid():
            patform=form.save(commit=False)
            patform.save()
            patform.involved_depts.add(request.POST.get('current_stage'))
            for test in tests:
                LabLog.objects.create(
                    lab_log_id = createId(LabLog,LabLog.lab_log_id,'TST'),
                    user = request.user,
                    service_log = test,
                    quantity = test.quantity,
                    pat_log = patform,
                    findings = patform.test_results,
                    cleared = True
                )
            messages.success(request,'Patient data updated successfully!')
            return redirect('investigations-uncompleted')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

    page_title = 'Patient File | Lab'
    context = {'page_title':page_title,'patientlog':patientLogFile,'departments':departments,'tests':tests}
    return render(request,'base/investigations/patient-file.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def adminSettings(request):
    page_title = 'Hospital Settings'
    context = {'page_title':page_title}
    return render(request,'base/hosp-settings/hosp-settings.html',context)
#the following functions handle listing of all objects associated with settings
'''
every function renders a keyword; for page heading, and a multidimensional list consisting of fields to be displayed in the following format: all_records[object_field[]]
'''
@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingDepartments(request):
    all_objs = Department.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.name)
        records_list.append(sub)
    page_title = 'Departments'
    message = "Existing departments can only be edited but not deleted."
    keyword = 'department'
    fields = {'#':'id','department':'name'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields,'message':message}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingLeaveStatuses(request):
    all_objs = LeaveStatus.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.status_code)
        sub.append(s.status_description)
        records_list.append(sub)
    page_title = 'Leave Statuses'
    keyword = 'leave_status'
    fields = {'#':'id','Status Code':'status_code','Description':'status_description'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingLeaveTypes(request):
    all_objs = LeaveType.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.leave_type)
        sub.append(s.leave_description)
        records_list.append(sub)
    page_title = 'Leave Types'
    keyword = 'leave_type'
    fields = {'#':'id','Leave Type':'leave_type','Description':'leave_description'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingCreditors(request):
    all_objs = PayerScheme.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.payer_name)
        sub.append(s.payer_class)
        records_list.append(sub)
    page_title = 'Creditors And Payer Schemes'
    keyword = 'creditor'
    fields = {'#':'id','Name':'payer_name','Grouping':'payer_class'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingFacility(request):
    all_objs = Facility.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.facility_name)
        sub.append(s.facility_location)
        sub.append(s.facility_phone)
        sub.append(s.facility_level)
        records_list.append(sub)
    page_title = 'Edit Facility Settings'
    keyword = 'facility'
    fields = {'#':'id','Name':'payer_name','Location':'facility_location','Tel':'facility_phone','Level':'facility_level'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingServices(request):
    all_services = Service.objects.all()
    records_list=[]
    fields = {'#':'id','Service':'service_name','Charge':'service_charge','Department':'department','Income Group':'service_group'}
    for s in all_services:
        sub=[]
        sub.append(s.id)
        sub.append(s.service_name)
        sub.append(s.service_charge)
        sub.append(s.department)
        sub.append(s.service_group)
        records_list.append(sub)
    page_title = 'Services'
    keyword = 'service'
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingPaymentModes(request):
    all_objs = PaymentMode.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.mode_name)
        sub.append(s.mode_class)
        records_list.append(sub)
    page_title = 'Edit Payment Settings'
    keyword = 'payment_mode'
    fields = {'#':'id','Name':'mode_name','Category':'mode_class'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingCashOptions(request):
    all_objs = CashOption.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.option_name)
        sub.append(s.parent_payer)
        records_list.append(sub)
    page_title = 'Edit Cash Option Settings'
    keyword = 'cash_option'
    fields = {'#':'id','Name':'option_name','Payer':'parent_payer'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingPettyCash(request):
    all_objs = ExpenseCategory.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.name)
        sub.append(s.description)
        records_list.append(sub)
    page_title = 'Edit Petty Cash Accounts'
    keyword = 'petty_cash'
    fields = {'#':'id','Name':'name','Description':'description'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingSuppliers(request):
    all_objs = Supplier.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.supplier_name)
        sub.append(s.location)
        sub.append(s.phone)
        records_list.append(sub)
    page_title = 'Edit Suppliers Listings'
    keyword = 'supplier'
    fields = {'#':'id','Name':'supplier_name','Location':'location','Phone Number':'phone'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingFinancialAccounts(request):
    all_objs = FinancialAccount.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.account_name)
        sub.append(s.amount_available)
        records_list.append(sub)
    page_title = 'Edit Financial Accounts Settings'
    keyword = 'financial_account'
    fields = {'#':'id','Name':'account_name','Amount Available':'amount_available'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingWards(request):
    all_objs = Ward.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.name)
        sub.append(s.category)
        sub.append(s.bed_count)
        sub.append(s.description)
        records_list.append(sub)
    page_title = 'Edit Ward Details'
    keyword = 'ward'
    fields = {'#':'id','Name':'name','Category':'category','beds':'bed_count','Description':'description'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsListingEmergencyCodes(request):
    all_objs = EmergencyCode.objects.all()
    records_list=[] 
    for s in all_objs:
        sub=[]
        sub.append(s.id)
        sub.append(s.code_name)
        sub.append(s.code_number)
        sub.append(s.code_description)
        records_list.append(sub)
    page_title = 'Edit Emergency Codes Settings'
    keyword = 'emergency_code'
    fields = {'#':'id','Name':'code_name','Priority':'code_number','Description':'code_description'}
    context = {'page_title':page_title,'records_list':records_list,'keyword':keyword,'fields':fields}
    return render(request,'base/hosp-settings/settings-listings.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsEdit(request,table,pk):
    t=str(table).lower()
    obj=None
    form_inst=None
    keyword=''
    deletable = True
    after_submit = 'admin-settings'
    if t=='leave_type':
        obj = LeaveType.objects.get(id=pk)
        form = LeaveTypeForm(instance=obj)
        form_inst = LeaveTypeForm
        keyword = t
        after_submit = 'admin-settings-leave-types'
    elif t=='leave_status':
        obj = LeaveStatus.objects.get(id=pk)
        form = LeaveStatusForm(instance=obj)
        form_inst = LeaveStatusForm
        keyword = t
        after_submit = 'admin-settings-leave-statuses'
    elif t=='department':
        obj = Department.objects.get(id=pk)
        form = DepartmentForm(instance=obj)
        form_inst = DepartmentForm
        keyword = t
        deletable = False
        after_submit = 'admin-settings-departments'
    elif t=='service':
        obj = Service.objects.get(id=pk)
        form = ServiceForm(instance=obj)
        form_inst = ServiceForm
        keyword = t
        after_submit = 'admin-settings-services'
    elif t=='facility':
        obj = Facility.objects.get(id=pk)
        form = FacilityForm(instance=obj)
        form_inst = FacilityForm
        keyword = t
        after_submit = 'admin-settings-facilities'
    elif t=='creditor':
        obj = PayerScheme.objects.get(id=pk)
        form = CreditorForm(instance=obj)
        form_inst = CreditorForm
        keyword = t
        after_submit = 'admin-settings-creditors'
    elif t=='payment_mode':
        obj = PaymentMode.objects.get(id=pk)
        form = PaymentModeForm(instance=obj)
        form_inst = PaymentModeForm
        keyword = t
        after_submit = 'admin-settings-payment-modes'
    elif t=='financial_account':
        obj = FinancialAccount.objects.get(id=pk)
        form = FinancialAccountForm(instance=obj)
        form_inst = FinancialAccountForm
        keyword = t
        after_submit = 'admin-settings-financial-accounts'
    elif t=='cash_option':
        obj = CashOption.objects.get(id=pk)
        form = CashOptionForm(instance=obj)
        form_inst = CashOptionForm
        keyword = t
        after_submit = 'admin-settings-cash-options'
    elif t=='petty_cash':
        obj=ExpenseCategory.objects.get(id=pk)
        form = ExpenseCategoryForm(instance=obj)
        form_inst = ExpenseCategoryForm
        keyword = t
        after_submit = 'admin-settings-petty-cash'
    elif t=='emergency_code':
        obj = EmergencyCode.objects.get(id=pk)
        form = EmergencyCodeForm(instance=obj)
        form_inst = EmergencyCodeForm
        keyword = t
        after_submit = 'admin-settings-emergency-codes'
    elif t=='supplier':
        obj = Supplier.objects.get(id=pk)
        form = SupplierForm(instance=obj)
        form_inst = SupplierForm
        keyword = t
        after_submit = 'admin-settings-suppliers'
    elif t=='ward':
        obj = Ward.objects.get(id=pk)
        form = WardForm(instance=obj)
        form_inst = WardForm
        keyword = t
        after_submit = 'admin-settings-wards'
    else:
        return HttpResponse('Check your request and try again')
    
    if request.method == 'POST':
        form = form_inst(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,str(obj)+' has been updated successfully.')
            return redirect(after_submit)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            
    page_title = 'Edit '+keyword
    context = {'page_title':page_title,'form':form,'keyword':keyword,'obj':obj,'deletable':deletable}
    return render(request,'base/hosp-settings/edit-item-form.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsAdd(request,table):
    t=str(table).lower()
    obj=None
    form_inst=None
    keyword=''
    after_submit = 'admin-settings'
    if t=='leave_type':
        obj = LeaveType
        form = LeaveTypeForm()
        form_inst = LeaveTypeForm
        keyword = t
        after_submit = 'admin-settings-leave-types'
    elif t=='leave_status':
        obj = LeaveStatus
        form = LeaveStatusForm()
        form_inst = LeaveStatusForm
        keyword = t
        after_submit = 'admin-settings-leave-statuses'
    elif t=='department':
        obj=Department
        form = DepartmentForm()
        form_inst = DepartmentForm
        keyword = t
        after_submit = 'admin-settings-departments'
    elif t=='service':
        obj=Service
        form = ServiceForm()
        form_inst = ServiceForm
        keyword = t
        after_submit = 'admin-settings-services'
    elif t=='facility':
        obj=Facility
        form = FacilityForm()
        form_inst = FacilityForm
        keyword = t
        after_submit = 'admin-settings-facilities'
    elif t=='creditor':
        obj=PayerScheme
        form = CreditorForm()
        form_inst = CreditorForm
        keyword = t
        after_submit = 'admin-settings-creditors'
    elif t=='payment_mode':
        obj=PaymentMode
        form = PaymentModeForm()
        form_inst = PaymentModeForm
        keyword = t
        after_submit = 'admin-settings-payment-modes'
    elif t=='financial_account':
        obj=FinancialAccount
        form = FinancialAccountForm()
        form_inst = FinancialAccountForm
        keyword = t
        after_submit = 'admin-settings-financial-accounts'
    elif t=='cash_option':
        obj=CashOption
        form = CashOptionForm()
        form_inst = CashOptionForm
        keyword = t
        after_submit = 'admin-settings-cash-options'
    elif t=='petty_cash':
        obj=ExpenseCategory
        form = ExpenseCategoryForm()
        form_inst = ExpenseCategoryForm
        keyword = t
        after_submit = 'admin-settings-petty-cash'
    elif t=='emergency_code':
        obj=EmergencyCode
        form = EmergencyCodeForm()
        form_inst = EmergencyCodeForm
        keyword = t
        after_submit = 'admin-settings-emergency-codes'
    elif t=='supplier':
        obj = Supplier
        form = SupplierForm()
        form_inst = SupplierForm
        keyword = t
        after_submit = 'admin-settings-suppliers'
    elif t=='ward':
        obj = Ward
        form = WardForm()
        form_inst = WardForm
        keyword = t
        after_submit = 'admin-settings-wards'
    else:
        return HttpResponse('Check your request and try again')
    
    if request.method == 'POST':
        form = form_inst(request.POST,request.FILES)
        if form.is_valid():
            rec_form=form.save(commit=False)
            rec_form.rec_id=createId(obj,obj.rec_id,'REC')
            rec_form.added_by=request.user
            rec_form.save()
            messages.success(request,str(rec_form)+' has been saved successfully.')
            return redirect(after_submit)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    page_title = 'Edit '+keyword
    context = {'page_title':page_title,'form':form,'keyword':keyword}
    return render(request,'base/hosp-settings/edit-item-form.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def settingsDelete(request,table,pk):
    t=str(table).lower()
    obj=None
    form_inst=None
    keyword=''
    ok = True
    after_submit = 'admin-settings'
    if t=='leave_type':
        obj = LeaveType.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-leave-types'
    elif t=='leave_status':
        obj = LeaveStatus.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-leave-statuses'
    elif t=='department':
        obj = Department.objects.get(id=pk)
        keyword = t
        ok = False
        messages.error(request,'Existing departments cannot be deleted. Please try renaming or deactivating instead.')
        after_submit = 'admin-settings-departments'
    elif t=='service':
        obj = Service.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-services'
    elif t=='facility':
        obj = Facility.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-facilities'
    elif t=='creditor':
        obj = PayerScheme.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-creditors'
    elif t=='payment_mode':
        obj = PaymentMode.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-payment-modes'
    elif t=='financial_account':
        obj = FinancialAccount.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-financial-accounts'
    elif t=='cash_option':
        obj = CashOption.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-cash-options'
    elif t=='petty_cash':
        obj = ExpenseCategory.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-petty-cash'
    elif t=='emergency_code':
        obj = EmergencyCode.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-emergency-codes'
    elif t=='supplier':
        obj = Supplier.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-suppliers'
    elif t=='ward':
        obj = Ward.objects.get(id=pk)
        keyword = t
        after_submit = 'admin-settings-wards'
    else:
        return HttpResponse('Check your request and try again')
    
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid() and ok:
            obj_name = str(obj)
            obj.delete()
            messages.success(request,obj_name+' has been deleted successfully.')
            return redirect(after_submit)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
        
    page_title = 'Delete '+keyword
    context = {'page_title':page_title,'keyword':keyword,'obj':obj}
    return render(request,'base/hosp-settings/edit-item-form.html',context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def group_permissions_view(request):
    # Retrieve all groups
    groups = Group.objects.all()
    members = {} 
    group_permissions = {}

    for group in groups:
        user_list = []
        users = group.user_set.all()
        for user in users:
            user_list.append(user)
        permissions = Permission.objects.filter(group=group)
        group_permissions[group] = permissions
        members[group] = user_list
    page_title = 'Groups & Permissions'
        
    context = {'group_permissions': group_permissions,'page_title':page_title,'members': members}
    return render(request, 'base/hosp-settings/group-permissions.html', context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def edit_group_permissions(request, pk):
    group = get_object_or_404(Group, pk=pk)
    all_permissions = Permission.objects.all()

    if request.method == 'POST':
        selected_permissions = request.POST.getlist('permissions')
        group.permissions.set(selected_permissions)
        return redirect('admin-settings-groups')  # Redirect to a page showing all groups and permissions

    page_title = 'Edit Group Permissions'
    context = {'page_title':page_title,'group': group,'all_permissions': all_permissions}
    return render(request, 'base/hosp-settings/edit-group-permissions.html', context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def create_group(request):
    all_permissions = Permission.objects.all()

    if request.method == 'POST':
        group_name = request.POST['group_name']
        selected_permissions = request.POST.getlist('permissions')
        
        group = Group.objects.create(name=group_name)
        group.permissions.set(selected_permissions)
        
        return redirect('admin-settings-groups')  # Redirect to a page showing all groups and permissions

    page_title = 'Create New Group'
    context = {'page_title':page_title,'all_permissions': all_permissions}
    return render(request, 'base/hosp-settings/create-group.html', context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def add_users_to_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_users = group.user_set.all()
    all_users = User.objects.all()
    form = AddUsersToGroupForm()

    if request.method == 'POST':
        form = AddUsersToGroupForm(request.POST, initial={'users': group_users})
        if form.is_valid():
            selected_users = form.cleaned_data['users']
            group.user_set.set(selected_users)
            return redirect('admin-settings-groups')

    page_title = 'Add Users To Group'
    context = {'page_title':page_title,'form': form,'group': group,'group_users': group_users,'all_users': all_users,}
    return render(request, 'base/hosp-settings/add-users-to-group.html', context)

@login_required(login_url="login")
@user_passes_test(is_admin,login_url="login")
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        obj_name = group.name
        group.delete()
        messages.success(request,obj_name+' group has been deleted successfully.')
        return redirect('admin-settings-groups')
    page_title = 'Delete Group'
    context = {'page_title':page_title,'group': group,}
    return render(request, 'base/hosp-settings/edit-group-permissions.html', context)