from django.contrib.auth.decorators import login_required
from django.db.models import Q
from base64 import b64encode, b64decode
from .models import Prescription,Patient,User,Drug,PatientLog,Service,ServiceLog,EmergencyCode,Facility,Department,DrugStockTake,PaymentMode,PayerScheme,ServiceAndPrescriptionLog,LabLog,ImagingLog,DentalLog,CashOption,DebitPaymentLog,Employee,LeaveStatus,LeaveType,EmployeeLeave,AttendanceLog,EmployeeEvaluation,FinancialAccount,Payroll,Supplier
from django.contrib import messages
import re
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.utils import timezone

# def encrypt_text(key, text):
#     cipher = AES.new(key, AES.MODE_ECB)
#     padded_text = pad(text.encode('utf-8'), AES.block_size)
#     encrypted_bytes = cipher.encrypt(padded_text)
#     encrypted_text = b64encode(encrypted_bytes).decode('utf-8')
#     return encrypted_text

# def decrypt_text(key, encrypted_text):
#     cipher = AES.new(key, AES.MODE_ECB)
#     encrypted_bytes = b64decode(encrypted_text)
#     decrypted_bytes = cipher.decrypt(encrypted_bytes)
#     decrypted_text = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
#     return decrypted_text

def RemovePrefix(index,prefix):
    s=str(index)
    if s !='':
        if prefix in str(s):
            res = int(str(s).replace(prefix,''))
        else:
            res = int(re.search(r'\d+', s).group())
    else:
        res = 1
    return res

def addPrefix(prefix,index):
    if (index<10):
        res= str(prefix)+"00"+str(index)
        return res

    elif(index>=10):
        res = str(prefix)+"0"+str(index)
        return res



def createId(table,fieldname,prefix)->str:
    '''
    Creates unique id values for objects in the database, by checking and incrementing the integer part of the field with the highest value.

    @param `table` - name of class or table as stored in database
    @param `preffix` - the preceeding initials that are constant for all fields

    e.g `createId(User,'USID')` checks the integer part of the highest `UID` and returns `USID001` if the table was empty.

    '''
    fieldname = str(fieldname)
    idsArray = [0]
    if table.objects.all().count() > 0:
        tableFields = table.objects.latest('created')
        idsArray.append(tableFields.field_id())
    else:
        tableFields = None

    idPrefix=prefix
    dm_adms = [0]
    for field in idsArray:
        newRow = field
        index = RemovePrefix(newRow,idPrefix)
        newRow = int(index)
        dm_adms.append(newRow)
    
    cur_max = max(dm_adms)
    
    if cur_max==1:
        newId = str(idPrefix)+"002"
    
    else:
        newId =cur_max+1
        index1 = addPrefix(idPrefix,newId)
        newId = index1

    return newId


def createOp(table,fieldname,preffix)->str:
    '''
    Functionality is similar to CreateId function
    '''
    fieldname = str(fieldname)
    idsArray = [0]
    if table.objects.all().count() > 0:
        tableFields = table.objects.latest('created')
        idsArray.append(tableFields.field_op())
    else:
        tableFields = None
    idPreffix=preffix
    dm_adms = [0]
    for field in idsArray:
        newRow = field
        index = RemovePrefix(newRow,idPreffix)
        newRow = int(index)
        dm_adms.append(newRow)
    cur_max = max(dm_adms)
    if cur_max==1:
        newId = str(idPreffix)+"002"
    else:
        newId =cur_max+1
        index1 = addPrefix(idPreffix,newId)
        newId = index1
    return newId

def get_visit_number(patientId):
    vn = 1
    if Patient.objects.filter(id=patientId).exists:
        pat = Patient.objects.get(id=patientId)
        vn = PatientLog.objects.filter(patient=pat).count()
        vn+=1
    return vn

def createPrescription(patlog,drug_id,quantity,price,dosage,frequency):
    prescription = None
    if PatientLog.objects.filter(id=patlog.id).exists():
        doctor = patlog.doctor
    if User.objects.filter(id=doctor.id).exists() and PatientLog.objects.filter(id=patlog.id).exists() and Drug.objects.filter(id=drug_id).exists():
        pat = PatientLog.objects.get(id=patlog.id)
        doc = User.objects.get(id=doctor.id)
        med = Drug.objects.get(id=drug_id)
        prescription = Prescription.objects.create(
            prcp_id = createId(Prescription,Prescription.prcp_id,'PRC'),
            patient = pat.patient,
            user = doc,
            patlog = pat,
            drug = med,
            quantity = quantity,
            price = price,
            dosage = dosage,
            frequency = frequency,
        )
        prescription.total_amount = prescription.get_total_price()
        prescription.save()
        drugrec = Drug.objects.get(id=prescription.drug.id)
        drugrec.quantity -= prescription.quantity
        drugrec.save()
    return prescription

def createServiceLog(patlogid,userid,serviceid):
    res = None
    if PatientLog.objects.filter(id=patlogid).exists() and User.objects.filter(id=userid).exists() and Service.objects.filter(id=serviceid).exists:
        patlog_obj = PatientLog.objects.get(id=patlogid)
        user_obj = User.objects.get(id=userid)
        service_obj = Service.objects.get(id=serviceid)
        res = ServiceLog.objects.create(
            sl_id = createId(ServiceLog,ServiceLog.sl_id,'SRL'),
            patient = patlog_obj.patient,
            patient_log = patlog_obj,
            user = user_obj,
            service = service_obj,
            quantity = 1,
            price = service_obj.service_charge,
        )
        res.total_amount = res.get_total_price()
        res.save()
    return res

def raise_emergency(request,code_id,trigger):
    emc_code = EmergencyCode.objects.get(id=code_id)
    # trigger_user = User.objects.filter(id=trigger.id)
    depts = emc_code.code_responders.all()
    # for dept in emc_code.code_responders:
    #     print(dept)
    for dept in depts:
        dept_users = User.objects.filter(department=dept)
        for user in dept_users:
            messages.error(request,str(emc_code.code_name)+" has been raise by "+str(trigger)+" in "+str(dept.name))
    return

# Define a user test for admin users
def is_admin(user):
    return user.is_superuser


# the following functions are unrelated to the project
def is_pangram(s):
    alph = list('abcdefghijklmnopqrstuvwxyz')
    new_list=[]
    s = list(s.lower())
    for i in alph:
        if i in list(s):
            new_list.append(i)
    return len(alph)==len(new_list)
def is_pangram2(s):
    return True if set('abcdefghijklmnopqrstuvwxyz').issubset(set(s.lower())) else False

def duplicate_encode(word):
    #your code here
    new_list = []
    for c in list(word.lower()):
        if len(word.lower().split(c))-1 > 1:
            new_list.append(')')
        else:
            new_list.append('(')
    return "".join(new_list)
def duplicate_encode2(word):
    return "".join(["(" if word.lower().count(c) == 1 else ")" for c in word.lower()])
# print(duplicate_encode('success'))

def gen_random(range_start,range_end,limit):
    from random import randrange
    a = []
    for c in range(limit):
        a.append(randrange(range_start,range_end))
        c+=1
    return a

# print(sorted(gen_random(0,1000,10)))

# create this sorting algorithm, in many different ways
# def sort(arr)->list:
#     new_arr = []
#     for i in arr:
#         if len(new_arr) == 0:
#             new_arr.append(i)
#         else:

def create_groups():
    models = {'patient':Patient,'user':User,'Facility':Facility,'Department':Department,'EmergencyCode':EmergencyCode,'Drug':Drug,'DrugStockTake':DrugStockTake,'Service':Service,'PaymentMode':PaymentMode,'LabLog':LabLog,'PayerScheme':PayerScheme,'Prescription':Prescription,'ServiceLog':ServiceLog,'PatientLog':PatientLog,'ServiceAndPrescriptionLog':ServiceAndPrescriptionLog,'ImagingLog':ImagingLog,'DentalLog':DentalLog,'CashOption':CashOption,'DebitPaymentLog':DebitPaymentLog,'Employee':Employee,'LeaveStatus':LeaveStatus,'LeaveType':LeaveType,'EmployeeLeave':EmployeeLeave,'AttendanceLog':AttendanceLog,'EmployeeEvaluation':EmployeeEvaluation,'FinancialAccount':FinancialAccount,'Payroll':Payroll,'Supplier':Supplier}
    # Create or retrieve the Receptionist group
    receptionist_group, created = Group.objects.get_or_create(name='Receptionist')
    if created:
        # Assign permissions to the Receptionist group for Patient model
        patient_content_type = ContentType.objects.get_for_model(Patient)
        receptionist_patient_permissions = Permission.objects.filter(
            content_type=patient_content_type,
            codename__in=['add_patient','view_patient', 'change_patient']
        )
        receptionist_group.permissions.set(receptionist_patient_permissions)
        
def user_perms(dpt):
    perms={
        'reception':['base.view_patient','base.change_patient','base.add_patientlog'],
        'cashier':['base.view_patient','base.change_patient','base.change_patientlog','base.change_debitpaymentlog'],
        'doctor':['base.view_patient','base.change_patient','base.change_patientlog','base.add_prescription','base.delete_prescription','base.change_prescription','base.add_servicelog','base.change_servicelog','base.delete_servicelog'],
        'pharmacy':['base.view_patientlog','base.change_patientlog','base.add_prescription','base.delete_prescription','base.change_prescription','base.change_drug','base.add_drug','base.delete_drug'],
        'lab':['base.view_patientlog','base.change_patientlog','base.add_lablog','base.delete_lablog','base.change_lablog'],
        'imaging':['base.view_patientlog','base.change_patientlog','base.add_imaginglog','base.delete_imaginglog','base.change_imaginglog'],
        'dental':['base.view_patientlog','base.change_patientlog','base.add_dentallog','base.delete_dentallog','base.change_dentallog'],
        'hr':['base.view_patient','base.add_attendancelog','base.change_attendancelog','base.delete_attendancelog','base.view_attendancelog','base.add_employeeevaluation','base.change_employeeevaluation','base.view_employeeevaluation','base.view_employeeevaluation','base.add_employee','base.change_employee','base.view_employee','base.delete_employee','base.add_employeeleave','base.view_employeeleave','base.change_employeeleave','base.delete_employeeleave','base.add_leavetype','base.view_leavetype','base.change_leavetype','base.delete_leavetype','base.add_payroll','base.view_payroll','base.change_payroll','base.delete_payroll'],
        'nurse':['base.view_patientlog','base.change_patientlog','base.add_lablog','base.change_lablog'],
        'finance':['base.add_payroll','base.view_payroll','base.change_payroll','base.delete_payroll'],
    }
    return perms[dpt]

def has_custom_permissions(request, required_permissions):
    cached_permissions = set(request.session.get('cached_permissions', []))
    print(request.session.get('cached_permissions'))
    return all(permission in cached_permissions for permission in required_permissions)

def daily_departmental_income(dpt):
    current_date = timezone.localdate()
    items = ServiceLog.objects.filter(created__date = current_date,service__department = dpt)
    department_total=0
    #geting total service and procedure income from departments
    for s in items:
        department_total+=s.total_amount
    return department_total

def daily_pharmacy_income():
    current_date = timezone.localdate()
    prescriptions = Prescription.objects.filter(created__date = current_date)
    pharmacy_amount = 0
    #geting total from drugs income
    for p in prescriptions:
        pharmacy_amount+=p.total_amount
    return pharmacy_amount