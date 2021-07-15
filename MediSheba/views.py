from django.http import HttpResponse
from django.shortcuts import render, redirect
import cx_Oracle

import HelperClasses.encryptPass as decoder_encoder
from HelperClasses import json_extractor
from HelperClasses import day_name
from HelperClasses import sequential_date_generator

from .models import DoctorName
from .models import BloodBankList
from .models import HospitalName
from .models import HospitalCabinName
from .models import CabinName
from .models import UserAppointment_in_blood_bank
from .models import userCabinHistory
from .models import doctor_user_history
from .models import cabinBookingDetails
from .models import Todays_Appointments
from .models import cabinBookingHistory

# login
user_info = {}  # holds user data across pages


def login(request):
    return render(request, "auth/LogInOrSignUp.html")


def signup(request):
    return render(request, "auth/SignUp.html")


# homepage URLs
def doctor_home(request):
    return render(request, "homepage/DoctorHome.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})


def user_home(request):
    return render(request, "homepage/UserHome.html", {'name': user_info['f_name'] + ' ' + user_info['l_name']})


def hospital_admin_home(request):
    return render(request, 'homepage/HospitalAdminHome.html', {'name': user_info['f_name'] + ' ' + user_info['l_name']})


def blood_bank_admin_home(request):
    return render(request, 'homepage/Blood_Bank_Home.html', {'name': user_info['f_name'] + ' ' + user_info['l_name']})


# log in

def submit(request):
    email = request.POST['email']
    password = request.POST['pass']
    user = request.POST['User']


    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

    c = conn.cursor()

    if user == "Doctor":
        statement = "SELECT DOCTOR_ID, PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.DOCTOR WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "doctor"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("doctor_home")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "User":
        statement = "SELECT USER_ID, PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.USERS WHERE EMAIL=" + "\'" + email + "\'"

        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "user"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("user_home")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "HospitalAdmin":
        statement = "SELECT HOSPITAL_ID,PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.HOSPITAL WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "hospital_admin"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("hospital_admin_home")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")

    elif user == "BloodBankAdmin":
        statement = "SELECT BLOOD_BANK_ID,PASSWORD, FIRST_NAME, LAST_NAME from MEDI_SHEBA.BLOOD_BANK WHERE EMAIL=" + "\'" + email + "\'"
        c.execute(statement)
        if c:
            x = c.fetchone()
            return_id = x[0]
            return_password = x[1]
            return_f_name = x[2]
            return_l_name = x[3]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "blood_bank_admin"

            decoded_password = decoder_encoder.EncryptPasswords(return_password).decryptPassword()

            if decoded_password == password:
                return redirect("blood_bank_admin_home")
            else:
                return HttpResponse("Wrong Pass")
        else:
            return HttpResponse("Database Error or You don't exist")
    return render(request, "auth/LogInOrSignUp.html")


# signup


def signupSubmit(request):
    usertype = request.POST['User']
    firstname = request.POST['fname']
    lastname = request.POST['lname']
    email = request.POST['email']
    phone = request.POST['phone']
    password_in = request.POST['pass']
    confirm_in = request.POST['cpass']
    gender_in = request.POST['Gender']
    blood_bank_name = hospital_name = request.POST['company']

    password = decoder_encoder.EncryptPasswords(password_in).encryptPassword()

    gender = ""
    if gender_in == "male":
        gender = "M"
    else:
        gender = "F"

    if usertype == 'doctor':

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        c2 = conn.cursor()
        c3 = conn.cursor()

        statement = "INSERT INTO MEDI_SHEBA.DOCTOR(FIRST_NAME, LAST_NAME, EMAIL, PHONE,PASSWORD, GENDER) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + phone + "\', " + "\'" + password + "\', " + "\'" + gender + "\'" + ")"
        c.execute(statement)
        conn.commit()

        statement = "SELECT DOCTOR_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.DOCTOR WHERE EMAIL=" + "\'" + email + "\'"
        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "doctor"

            # statement = "INSERT INTO MEDI_SHEBA.DOCTOR_SCHEDULE(DOCTOR_ID) VALUES (" + str(user_info['pk']) + ")"

            # TODO: DOCTOR SCHEDULE INSERT SQL FUNCTION HERE
            id = [return_id]
            result = c3.callfunc('insert_into_doctor_schedule', str, id)
            print(result)

            # c3.execute(statement)
            # conn.commit()

            return redirect("doctor_home")
        else:
            return HttpResponse("ERROR")  # changed here


    elif usertype == 'user':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO MEDI_SHEBA.USERS(FIRST_NAME, LAST_NAME, EMAIL, PHONE,PASSWORD, GENDER) VALUES (" + "\'" + firstname + \
                    "\', " + "\'" + lastname + "\'," + "\'" + email + "\', " + "\'" + phone + "\', " + "\'" + password + "\', " + "\'" + gender + "\'" + ")"
        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT USER_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.USERS WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "user"

            return redirect("user_home")
        else:
            return HttpResponse("ERROR")

    elif usertype == 'hospitalAdmin':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "INSERT INTO MEDI_SHEBA.HOSPITAL(HOSPITAL_NAME, FIRST_NAME, LAST_NAME, PASSWORD, GENDER, EMAIL, PHONE) VALUES" \
                    " (" + "\'" + hospital_name + "\'," + "\'" + firstname + "\'," + "\'" + lastname + "\'," + "\'" + password + "\'," + "\'" + gender \
                    + "\'," + "\'" + email + "\'," + "\'" + phone + "\'" + ")"

        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT HOSPITAL_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.HOSPITAL WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "hospital_admin"

            return redirect("hospital_admin_home")
        else:
            return HttpResponse("ERROR")

    elif usertype == 'bloodbankAdmin':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "INSERT INTO MEDI_SHEBA.BLOOD_BANK(NAME, FIRST_NAME, LAST_NAME, PASSWORD, GENDER, EMAIL, PHONE) " \
                    "VALUES" \
                    " (" + "\'" + blood_bank_name + "\'," + "\'" + firstname + "\'," + "\'" + lastname + "\'," + "\'" + password + "\'," + "\'" + gender \
                    + "\'," + "\'" + email + "\'," + "\'" + phone + "\'" + ")"

        c.execute(statement)
        conn.commit()

        c2 = conn.cursor()

        statement = "SELECT BLOOD_BANK_ID, FIRST_NAME, LAST_NAME from MEDI_SHEBA.BLOOD_BANK WHERE EMAIL=" + "\'" + email + "\'"

        c2.execute(statement)

        if c2:
            x = c2.fetchone()
            return_id = x[0]
            return_f_name = x[1]
            return_l_name = x[2]

            user_info['pk'] = return_id
            user_info['f_name'] = return_f_name
            user_info['l_name'] = return_l_name
            user_info['email'] = email
            user_info['type'] = "blood_bank_admin"

            return redirect("blood_bank_admin_home")

        else:
            return HttpResponse("ERROR")


# doctor

def doctor_edit_profile(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "doctor":
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
        c.execute(statement)

        hospital_names = []

        for i in c:
            hospital_names.append(i[0])

        location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
        location_names.sort()

        return render(request, 'profile_editor/DoctorProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def submit_changed_profile_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        phone_number = request.POST['phone']
        location = request.POST['address']
        email = request.POST['email']
        blood_type = request.POST['blood_type']
        hospital_name = request.POST['hospital_name']
        fee = request.POST['fee']
        specialization = request.POST['specialization']
        # additional_details = request.POST['additional_details']

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

        if first_name != "":
            c = conn.cursor()
            # statement = "UPDATE MEDI_SHEBA.DOCTOR SET FIRST_NAME = " + "\'" + first_name + "\'" + "WHERE DOCTOR_ID = " + str(user_info['pk'])
            # c.execute(statement)
            # conn.commit()
            data = [user_info['pk'], first_name]
            # TODO: UPDATE FUNCTION USED HERE
            result = c.callfunc('insert_doctors_first_name', str, data)
            print(result)
        else:
            print("First Name NOT CHANGED ")

        if last_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET LAST_NAME = " + "\'" + last_name + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LAST Name NOT CHANGED ")

        if phone_number != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET PHONE = " + "\'" + phone_number + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("PHONE NOT CHANGED ")

        if location != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET LOCATION = " + "\'" + location + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LOCATION NOT CHANGED ")

        if email != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET EMAIL = " + "\'" + email + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("EMAIL NOT CHANGED ")

        if blood_type != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET BLOOD_GROUP = " + "\'" + blood_type + "\'" + "WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("BLOOD NOT CHANGED ")

        if hospital_name != "":
            c = conn.cursor()
            statement_1 = "SELECT HOSPITAL_ID FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_NAME = " + "\'" + hospital_name + "\'"
            c.execute(statement_1)

            hospital_id = 0
            for r in c:
                hospital_id = r[0]

            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET HOSPITAL_ID = " + str(hospital_id) + " WHERE DOCTOR_ID = " \
                        + str(user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("HOSPITAL NOT CHANGED ")

        if fee != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET FEES = " + fee + " WHERE DOCTOR_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("FEES NOT CHANGED ")

        if specialization != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.DOCTOR SET SPECIALIZATION = " + "\'" + specialization + "\'" \
                        + " WHERE DOCTOR_ID = " + str(user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("SPECIALIZATION NOT CHANGED ")

        # TODO: HANDLE MULTI VALUE DICT KEY ERROR IF SOMETHING IS NOT GIVEN AS INPUT, SPECIALLY DROP DOWN BOXES

        c = conn.cursor()
        statement = "SELECT DOCTOR_ID, FIRST_NAME, LAST_NAME,EMAIL from MEDI_SHEBA.DOCTOR  WHERE DOCTOR_ID=" + str(
            user_info['pk'])
        c.execute(statement)
        if c:
            x = c.fetchone()
            id = x[0]
            f_name = x[1]
            l_name = x[2]
            email = x[3]
            user_info['pk'] = id
            user_info['f_name'] = f_name
            user_info['l_name'] = l_name
            user_info['email'] = email
        return redirect("doctor_home")
    else:
        return HttpResponse("Access not granted")


def doctor_search_options(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'homepage/Search_for_doctor.html')
    else:
        return HttpResponse("NO ACCESS")


def view_user_appointments_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'appointment_history_pages/doctor_history/doctor_user_history.html')
    else:
        return HttpResponse("NO ACCESS")


def past_appointment_of_user_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "SELECT U.USER_ID, U.FIRST_NAME, U.LAST_NAME, TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') FROM USERS U,DOCTOR_USER_HISTORY DUH WHERE DUH.USER_ID = U.USER_ID AND TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') < TO_CHAR((SELECT SYSDATE FROM DUAL),'yyyy-mm-dd') AND DUH.DOCTOR_ID =" + \
                    str(user_info['pk'])
        c.execute(statement)
        past_appointment_list = []
        index = 1
        for r in c:
            past_appointment_list.append(Todays_Appointments(index, r[0], user_info['pk'], r[1], r[2], r[3]))
            index = index + 1

        return render(request, 'appointment_history_pages/doctor_history/user/past_appointment_user.html',
                      {'past_appointment': past_appointment_list})
    else:
        return HttpResponse("NO ACCESS")


def upcoming_appointment_of_user_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "SELECT U.USER_ID, U.FIRST_NAME, U.LAST_NAME, TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') FROM USERS U,DOCTOR_USER_HISTORY DUH WHERE DUH.USER_ID = U.USER_ID AND TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') > TO_CHAR((SELECT SYSDATE FROM DUAL),'yyyy-mm-dd') AND DUH.DOCTOR_ID =" + \
                    str(user_info['pk'])
        c.execute(statement)
        future_appointment_list = []
        index = 1
        for r in c:
            future_appointment_list.append(Todays_Appointments(index, r[0], user_info['pk'], r[1], r[2], r[3]))
            index = index + 1
        return render(request, 'appointment_history_pages/doctor_history/user/upcoming_appointment_user.html',
                      {'upcoming_appointment': future_appointment_list})
    else:
        return HttpResponse("NO ACCESS")


def add_user_problem_prescription(request):
    user_id = request.POST.get("user_id", "No result")
    print(user_id)
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT FIRST_NAME, LAST_NAME, EMAIL FROM MEDI_SHEBA.USERS WHERE USER_ID = " + str(user_id)
    c.execute(statement)
    f_name = ""
    l_name = ""
    mail = ""
    for r in c:
        f_name = r[0]
        l_name = r[1]
        mail = r[2]
    return render(request, 'appointment_history_pages/doctor_history/user/add_problem_and_prescription.html',
                  {'name': f_name + " " + l_name,
                   'email': mail,
                   'user_id': user_id})


def add_problem_and_prescription(request):
    problem = request.POST.get("problem", "Not Specified")
    prescription = request.POST.get("prescription", "Not Specified")
    user_id = request.POST.get("user_id", "Not Specified")
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    statement = "UPDATE MEDI_SHEBA.DOCTOR_USER_HISTORY SET PROBLEM =" + "\'" + problem + "\'" + " WHERE DOCTOR_ID = " + str(
        user_info['pk']) + " AND USER_ID = " + str(
        user_id) + " AND TO_CHAR(APPOINTMENT_TIME,'yyyy-mm-dd') = TO_CHAR((SELECT SYSDATE FROM DUAL),'yyyy-mm-dd')"
    c.execute(statement)
    conn.commit()

    statement = "UPDATE MEDI_SHEBA.DOCTOR_USER_HISTORY SET PRESCRIPTION =" + "\'" + prescription + "\'" + " WHERE DOCTOR_ID = " + str(
        user_info['pk']) + " AND USER_ID = " + str(
        user_id) + " AND TO_CHAR(APPOINTMENT_TIME,'yyyy-mm-dd') = TO_CHAR((SELECT SYSDATE FROM DUAL),'yyyy-mm-dd')"
    c.execute(statement)
    conn.commit()

    return render(request, 'appointment_history_pages/doctor_history/user/done.html')


def todays_appointment_of_user_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()

        statement = "SELECT U.USER_ID, U.FIRST_NAME, U.LAST_NAME, TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') FROM USERS U,DOCTOR_USER_HISTORY DUH WHERE DUH.USER_ID = U.USER_ID AND TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') = TO_CHAR((SELECT SYSDATE FROM DUAL),'yyyy-mm-dd') AND DUH.DOCTOR_ID =" + \
                    str(user_info['pk'])
        c.execute(statement)
        todays_appointment_list = []
        index = 1
        for r in c:
            todays_appointment_list.append(Todays_Appointments(index, r[0], user_info['pk'], r[1], r[2], r[3]))
            index = index + 1

        return render(request, 'appointment_history_pages/doctor_history/user/todays_appointment_user.html',
                      {'todays_appointment': todays_appointment_list})
    else:
        return HttpResponse("NO ACCESS")


def view_doctor_appointments_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'appointment_history_pages/doctor_history/doctor_doctor_history.html')
    else:
        return HttpResponse("NO ACCESS")


# TODO: DOCTOR DOCTOR HISTORY
def past_appointment_of_doctor_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT D.DOCTOR_ID, D.FIRST_NAME, D.LAST_NAME, TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') FROM DOCTOR D,DOCTOR_USER_HISTORY DUH WHERE D.DOCTOR_ID = DUH.DOCTOR_ID AND DUH.USER_ID = " + str(
            user_info[
                'pk']) + " AND DUH.USER_TYPE = " + "\'" + "doctor" + "\'" + " AND TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') <= (SELECT TO_CHAR(SYSDATE,'yyyy-mm-dd') FROM DUAL)"

        c.execute(statement)
        past_appointment = []

        index = 1
        for r in c:
            past_appointment.append(doctor_user_history(index, user_info['pk'], r[0], r[1], r[2], r[3]))
            index = index + 1

        return render(request, 'appointment_history_pages/doctor_history/doctor/past_appointment_doctor.html',
                      {'past_appointment': past_appointment})
    else:
        return HttpResponse("NO ACCESS")


def upcoming_appointment_of_doctor_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT D.DOCTOR_ID, D.FIRST_NAME, D.LAST_NAME, TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') FROM DOCTOR D,DOCTOR_USER_HISTORY DUH WHERE D.DOCTOR_ID = DUH.DOCTOR_ID AND DUH.USER_ID = " + str(
            user_info[
                'pk']) + " AND DUH.USER_TYPE = " + "\'" + "doctor" + "\'" + " AND TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') < (SELECT TO_CHAR(SYSDATE,'yyyy-mm-dd') FROM DUAL)"

        c.execute(statement)
        upcoming_appointment = []

        index = 1
        for r in c:
            upcoming_appointment.append(doctor_user_history(index, user_info['pk'], r[0], r[1], r[2], r[3]))
            index = index + 1

        return render(request, 'appointment_history_pages/doctor_history/doctor/upcoming_appointment_doctor.html',
                      {'upcoming_appointment': upcoming_appointment})
    else:
        return HttpResponse("NO ACCESS")


def pending_appointment_of_doctor_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("pending not done")
    else:
        return HttpResponse("NO ACCESS")


def view_hospital_appointments_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'appointment_history_pages/doctor_history/doctor_hospital_history.html')
    else:
        return HttpResponse("NO ACCESS")


def past_appointment_of_hospital_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("past not done")
    else:
        return HttpResponse("NO ACCESS")


def upcoming_appointment_of_hospital_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("upcoming not done")
    else:
        return HttpResponse("NO ACCESS")


def pending_appointment_of_hospital_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("pending not done")
    else:
        return HttpResponse("NO ACCESS")


def view_bloodbank_appointments_by_doctor(request):
    return render(request, 'appointment_history_pages/doctor_history/blood_bank/bloodbank_appointment_options.html')


def past_appointment_of_bloodbank_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("past not done")
    else:
        return HttpResponse("NO ACCESS")


def upcoming_appointment_of_bloodbank_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("upcoming not done")
    else:
        return HttpResponse("NO ACCESS")


def pending_appointment_of_bloodbank_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return HttpResponse("pending not done")
    else:
        return HttpResponse("NO ACCESS")


def doctor_view_calender(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'schedule_editor/calendar2.html')
    else:
        return HttpResponse("NO ACCESS")


def doctor_view_records(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'homepage/records_for_doctor_table.html')
    else:
        return HttpResponse(" NO ACCESS")


def doctor_user_history_from_doctor(request):
    return render(request, 'appointment_history_pages/doctor_history/doctor_user_history.html')


def doctor_hospital_history_from_doctor(request):
    return render(request, 'appointment_history_pages/doctor_history/doctor_hospital_history.html')


def doctor_blood_bank_history_from_doctor(request):
    return render(request, 'appointment_history_pages/doctor_history/doctor_blood_bank_history.html')


def doctor_change_schedule(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return render(request, 'schedule_editor/AddSchedule.html')
    else:
        return HttpResponse("No ACCESS")


def logout(request):
    user_info.clear()
    return redirect("login")


def filter_search_doctor(request):
    specialization = request.POST.get('select_specialization', 'No Preferences')
    gender_return = request.POST.get('select_gender', 'No Preferences')
    area = request.POST.get('select_area', 'No Preferences')
    gender = gender_return
    if gender_return == "Male":
        gender = "M"
    elif gender_return == "Female":
        gender = "F"
    statement = ""
    if specialization == "No Preferences" and gender == "No Preferences" and area == "No Preferences":
        if user_info['type'] == "doctor":
            return redirect(search_doctors_by_doctor)
        elif user_info['type'] == "user":
            return redirect(search_doctors_by_user)
        elif user_info['type'] == "hospital_admin":
            return redirect(search_doctors_by_hospitals)
        elif user_info['type'] == "blood_bank_admin":
            return redirect(search_doctors_by_bloodbank)

    elif specialization == "No Preferences":
        if gender == "No Preferences":
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION= " + "\'" + area + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION= " + "\'" + area + "\'" + " AND DOCTOR_ID != " + str(
                    user_info['pk'])

        elif area == "No Preferences":
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER = " + "\'" + gender + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER = " + "\'" + gender + "\'" + " AND DOCTOR_ID != " + str(
                    user_info['pk'])

        else:
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER = " + "\'" + gender + "\'" + " AND  LOCATION = " + "\'" + area + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER = " + "\'" + gender + "\'" + " AND  LOCATION = " + "\'" + area + "\'" + " AND DOCTOR_ID != " + str(
                    user_info['pk'])

    elif gender == "No Preferences":
        if specialization == "No Preferences":
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION = " + "\'" + area + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION = " + "\'" + area + "\'" + " AND DOCTOR_ID !=" + str(
                    user_info['pk'])

        elif area == "No Preferences":
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION = " + "\'" + specialization + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION = " + "\'" + specialization + "\'" + " AND DOCTOR_ID != " + str(
                    user_info['pk'])
        else:
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION = " + "\'" + area + "\'" + " AND SPECIALIZATION =" + "\'" + specialization + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE LOCATION = " + "\'" + area + "\'" + " AND SPECIALIZATION =" + "\'" + specialization + "\'" + " AND DOCTOR_ID != " + str(
                    user_info['type'])

    elif area == "No Preferences":
        if specialization == "No Preferences":
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER= " + "\'" + gender + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE GENDER= " + "\'" + gender + "\'" + " AND DOCTOR_ID != " + str(
                    user_info['pk'])
        elif gender == "No Preferences":
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'" + " AND DOCTOR_ID != " + str(
                    user_info['pk'])
        else:
            if user_info['type'] != 'doctor':
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'" + " AND GENDER = " + "\'" + gender + "\'"
            else:
                statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'" + " AND GENDER = " + "\'" + gender + "\'" + " AND DOCTOR_ID !=" + str(
                    user_info['pk'])
    else:
        if user_info['type'] != 'doctor':
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'" + " AND GENDER = " + "\'" + gender + "\'" + " AND LOCATION = " + "\'" + area + "\'"
        else:
            statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE SPECIALIZATION= " + "\'" + specialization + "\'" + " AND GENDER = " + "\'" + gender + "\'" + " AND LOCATION = " + "\'" + area + "\'" + " AND DOCTOR_ID != " + str(
                user_info['pk'])

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    specialization_options = []
    docList = []

    # print(statement)
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(statement)
    index = 1
    for row in c:
        docList.append(DoctorName(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        index = index + 1
    c.execute("SELECT DISTINCT SPECIALIZATION FROM MEDI_SHEBA.DOCTOR")
    for row in c:
        specialization_options.append(row[0])
    conn.close()
    return render(request, 'query_pages/query_page_for_doctors/doctor_custom_query.html',
                  {'doc': docList, 'opt': location_names, 'specialization': specialization_options})


def custom_search_for_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return filter_search_doctor(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_doctor_by_user(request):
    if bool(user_info) and user_info['type'] == "user":
        return filter_search_doctor(request)
    else:
        return HttpResponse("NO ACCESS")


def custom_search_for_doctor_by_hospital_admin(request):
    if bool(user_info) and user_info['type'] == "hospital_admin":
        return filter_search_doctor(request)
    else:
        return HttpResponse("NO ACCESS")


def custom_search_for_doctor_by_blood_bank_admin(request):
    if bool(user_info) and user_info['type'] == "blood_bank_admin":
        return filter_search_doctor(request)
    else:
        return HttpResponse("NO ACCESS")


def search_doctors_by_doctor(request):
    return see_doctors(request)


def search_doctors_by_user(request):
    return see_doctors(request)


def search_doctors_by_bloodbank(request):
    return see_doctors(request)


def see_doctors(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    specialization = []

    docList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = ""
    if user_info['type'] == 'doctor':
        statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID from MEDI_SHEBA.DOCTOR WHERE DOCTOR_ID != " + str(
            user_info['pk'])
    else:
        statement = "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID from MEDI_SHEBA.DOCTOR"
    c.execute(statement)
    index = 1
    for row in c:
        docList.append(
            DoctorName(index, row[0], row[1], row[2], row[3], row[4], row[5],
                       row[6]))  # DoctorName is defined in models.py
        index = index + 1

    c.execute("SELECT DISTINCT SPECIALIZATION FROM MEDI_SHEBA.DOCTOR")
    for row in c:
        specialization.append(row[0])

    conn.close()

    return render(request, "query_pages/query_page_for_doctors/doctor_query.html",
                  {'doc': docList, 'opt': location_names, 'specialization': specialization})


def see_specific_doctor_details(request):
    doctor_id = request.POST['doctor_id']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    statement = "SELECT FIRST_NAME, LAST_NAME, PHONE, LOCATION, EMAIL, NVL(HOSPITAL_ID,-1), FEES, SPECIALIZATION FROM MEDI_SHEBA.DOCTOR WHERE DOCTOR_ID = " + str(
        doctor_id)
    c.execute(statement)

    first_name = ""
    last_name = ""
    phone = ""
    location = ""
    email = ""
    hospital_id = ""
    fees = ""
    specialization = ""
    msg = ""
    for row in c:
        first_name = row[0]
        last_name = row[1]
        phone = row[2]
        location = row[3]
        email = row[4]
        hospital_id = row[5]
        fees = row[6]
        specialization = row[7]
    hospital_full_name = ""

    if hospital_id != -1:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        c.execute("SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_ID = " + str(hospital_id))
        for row in c:
            hospital_full_name = row[0]
    else:
        hospital_full_name = "NONE"

    if user_info['type'] == 'user':
        return render(request, "detail_showing_pages/see_doctor_details_by_user/see_doctors_details.html",
                      {'name': first_name + " " + last_name, 'first_name': first_name,
                       'last_name': last_name, 'phone': phone, 'location': location, 'email': email,
                       'hospital_name': hospital_full_name, 'fees': fees, 'specialization': specialization,
                       'doctor_id': doctor_id,
                       'msg': msg})
    return render(request, "detail_showing_pages/see_doctors_details.html",
                  {'name': first_name + " " + last_name, 'first_name': first_name,
                   'last_name': last_name, 'phone': phone, 'location': location, 'email': email,
                   'hospital_name': hospital_full_name, 'fees': fees, 'specialization': specialization,
                   'doctor_id': doctor_id,
                   'msg': msg})


# TODO: APPOINTMENT FOR DOCTOR BY USER
def submit_appointment_for_doctor_by_user(request):
    doctor_id = request.POST.get("doctor_id", "none")
    selected_date = request.POST.get("appointment_date", "none")

    if selected_date == "none":
        return redirect("see_specific_doctor_details")

    print(doctor_id)
    print(selected_date)
    day = day_name.FindDayName(selected_date).find_day_name()
    print(day)

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT DOCTOR_ID, TO_CHAR(APPOINTMENT_DATE,'yyyy-mm-dd'), OCCUPIED, MAX_CAPACITY FROM MEDI_SHEBA.DOCTOR_APPOINTMENT_MANAGEMENT WHERE TO_CHAR(APPOINTMENT_DATE,'yyyy-mm-dd') = " + "\'" + selected_date + "\'" + " AND  DOCTOR_ID = " + str(
        doctor_id)
    c.execute(statement)
    date_list = []

    msg = ""

    occupied_slot = 0
    max_slot = 0
    for row in c:
        date_list.append(row[0])
        date_list.append(row[1])
        date_list.append(row[2])
        date_list.append(row[3])
        occupied_slot = row[2]
        max_slot = row[3]

    if bool(date_list):  # got some data from query, that means that the date already exists, now check for availability
        if occupied_slot == max_slot:
            print("No available slot on " + selected_date)
            print("Suggest a new date")
            print("If selected, add that date")
            msg = "No slot available on " + selected_date
            return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_failed.html')
        else:
            print(
                "Ok , found available slot on that DATE, increase occupied by 1 , add this appointment to doctor_user_history")
            occupied_slot = occupied_slot + 1
            query = "UPDATE MEDI_SHEBA.DOCTOR_APPOINTMENT_MANAGEMENT SET OCCUPIED = " + str(
                occupied_slot) + " WHERE DOCTOR_ID = " + str(
                doctor_id) + " AND APPOINTMENT_DATE = " + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')"
            c.execute(query)
            conn.commit()

            if user_info['type'] == 'user':
                query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                    doctor_id) + "," + str(user_info[
                                               'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "user" + "\'" + ")"
                c.execute(query)
                conn.commit()
            elif user_info['type'] == 'doctor':
                query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                    doctor_id) + "," + str(user_info[
                                               'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "doctor" + "\'" + ")"
                c.execute(query)
                conn.commit()
            return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_successful.html')
    else:
        print(" date NOT FOUND in database")
        print(" ADD THIS DATE ")
        max_capacity = 0
        if day == 'Saturday':
            statement1 = "SELECT SAT_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Sunday':
            statement1 = "SELECT SUN_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Monday':
            statement1 = "SELECT MON_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Tuesday':
            statement1 = "SELECT TUES_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Wednesday':
            statement1 = "SELECT WED_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Thursday':
            statement1 = "SELECT THU_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Friday':
            statement1 = "SELECT FRI_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]

        # insert in to appointment management
        query = "INSERT INTO MEDI_SHEBA.DOCTOR_APPOINTMENT_MANAGEMENT(DOCTOR_ID, APPOINTMENT_DATE, OCCUPIED, MAX_CAPACITY) VALUES (" \
                + str(doctor_id) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + str(
            1) + "," + str(max_capacity) + ")"
        print(query)
        c.execute(query)
        conn.commit()

        # insert in to doctor user history

        if user_info['type'] == 'user':
            query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                doctor_id) + "," + str(user_info[
                                           'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "user" + "\'" + ")"
            c.execute(query)
            conn.commit()
        elif user_info['type'] == 'doctor':
            query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                doctor_id) + "," + str(user_info[
                                           'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "doctor" + "\'" + ")"
            c.execute(query)
            conn.commit()
        return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_successful.html')


def go_to_your_home(request):
    if user_info['type'] == 'user':
        return redirect("user_home")
    elif user_info['type'] == 'doctor':
        return redirect("doctor_home")
    elif user_info['type'] == 'blood_bank_admin':
        return redirect("blood_bank_admin_home")


def submit_appointment_for_doctor_by_doctor(request):
    doctor_id = request.POST.get("doctor_id", "none")
    selected_date = request.POST.get("appointment_date", "none")

    if selected_date == "none":
        return redirect("see_specific_doctor_details")

    print(doctor_id)
    print(selected_date)
    day = day_name.FindDayName(selected_date).find_day_name()
    print(day)

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT DOCTOR_ID, TO_CHAR(APPOINTMENT_DATE,'yyyy-mm-dd'), OCCUPIED, MAX_CAPACITY FROM MEDI_SHEBA.DOCTOR_APPOINTMENT_MANAGEMENT WHERE TO_CHAR(APPOINTMENT_DATE,'yyyy-mm-dd') = " + "\'" + selected_date + "\'" + " AND  DOCTOR_ID = " + str(
        doctor_id)
    c.execute(statement)
    date_list = []
    msg = ""
    occupied_slot = 0
    max_slot = 0
    for row in c:
        date_list.append(row[0])
        date_list.append(row[1])
        date_list.append(row[2])
        date_list.append(row[3])
        occupied_slot = row[2]
        max_slot = row[3]

    if bool(date_list):  # got some data from query, that means that the date already exists, now check for availability
        if occupied_slot == max_slot:
            print("No available slot on " + selected_date)
            print("Suggest a new date")
            print("If selected, add that date")
            msg = "No Slot Available on " + selected_date
            return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_failed.html')
        else:
            print(
                "Ok , found available slot on that DATE, increase occupied by 1 , add this appointment to doctor_user_history")
            occupied_slot = occupied_slot + 1
            query = "UPDATE MEDI_SHEBA.DOCTOR_APPOINTMENT_MANAGEMENT SET OCCUPIED = " + str(
                occupied_slot) + " WHERE DOCTOR_ID = " + str(
                doctor_id) + " AND APPOINTMENT_DATE = " + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')"
            c.execute(query)
            conn.commit()

            if user_info['type'] == 'user':
                query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                    doctor_id) + "," + str(user_info[
                                               'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "user" + "\'" + ")"
                c.execute(query)
                conn.commit()
            elif user_info['type'] == 'doctor':
                query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                    doctor_id) + "," + str(user_info[
                                               'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "doctor" + "\'" + ")"
                c.execute(query)
                conn.commit()
            return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_successful.html')
    else:
        print(" date NOT FOUND in database")
        print(" ADD THIS DATE ")
        max_capacity = 0
        if day == 'Saturday':
            statement1 = "SELECT SAT_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Sunday':
            statement1 = "SELECT SUN_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Monday':
            statement1 = "SELECT MON_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Tuesday':
            statement1 = "SELECT TUES_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Wednesday':
            statement1 = "SELECT WED_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Thursday':
            statement1 = "SELECT THU_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        elif day == 'Friday':
            statement1 = "SELECT FRI_MAX FROM MEDI_SHEBA.DOCTOR_SCHEDULE WHERE DOCTOR_ID = " + str(doctor_id)
            c.execute(statement1)
            for r in c:
                max_capacity = r[0]
        # TODO: COPY DATE INSERT FROM HERE
        # insert in to appointment management
        query = "INSERT INTO MEDI_SHEBA.DOCTOR_APPOINTMENT_MANAGEMENT(DOCTOR_ID, APPOINTMENT_DATE, OCCUPIED, MAX_CAPACITY) VALUES (" + str(
            doctor_id) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + str(
            1) + "," + str(max_capacity) + ")"
        print(query)
        c.execute(query)
        conn.commit()

        # insert in to doctor user history

        if user_info['type'] == 'user':
            query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                doctor_id) + "," + str(user_info[
                                           'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "user" + "\'" + ")"
            c.execute(query)
            conn.commit()
        elif user_info['type'] == 'doctor':
            query = "INSERT INTO MEDI_SHEBA.DOCTOR_USER_HISTORY(DOCTOR_ID, USER_ID, APPOINTMENT_TIME, USER_TYPE) VALUES (" + str(
                doctor_id) + "," + str(user_info[
                                           'pk']) + "," + "TO_DATE(" + "\'" + selected_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + "doctor" + "\'" + ")"
            c.execute(query)
            conn.commit()
        return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_successful.html')


def submit_appointment(request):
    return HttpResponse("Appointment sent to doctor")


# USERS


# Hospital


def see_doctors_of_specific_hospital(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    hospital_id = request.POST['hospital_id_for_doctor']
    specialization = []

    docList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(
        "SELECT FIRST_NAME || ' ' || LAST_NAME,PHONE, GENDER, SPECIALIZATION, LOCATION, NVL(HOSPITAL_ID,-1), DOCTOR_ID FROM MEDI_SHEBA.DOCTOR WHERE HOSPITAL_ID = " + str(
            hospital_id))
    index = 1
    for row in c:
        docList.append(
            DoctorName(index, row[0], row[1], row[2], row[3], row[4], row[5],
                       row[6]))  # DoctorName is defined in models.py
        index = index + 1

    c.execute("SELECT DISTINCT SPECIALIZATION FROM MEDI_SHEBA.DOCTOR")
    for row in c:
        specialization.append(row[0])

    conn.close()

    return render(request, "query_pages/query_page_for_doctors/doctor_query.html",
                  {'doc': docList, 'opt': location_names, 'specialization': specialization})


def see_specific_hospital_details(request):
    hospital_id = request.POST['hospital_id']
    hospital_id_for_doctor = hospital_id
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    c.execute(
        "SELECT HOSPITAL_NAME, PHONE, LOCATION, EMAIL FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_ID = " + str(hospital_id))

    hospital_name = ""
    phone = ""
    location = ""
    email = ""
    hospital_id = ""

    for row in c:
        hospital_name = row[0]
        phone = row[1]
        location = row[2]
        email = row[3]

    return render(request, "detail_showing_pages/see_hospital_details.html",
                  {'name': hospital_name,
                   'phone': phone, 'location': location, 'email': email,
                   'hospital_id_for_doctor': hospital_id_for_doctor
                   })


def custom_search_for_hospital_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_hospital_by_bloodbank(request):
    if bool(user_info) and user_info['type'] == 'blood_bank_admin':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_hospital_by_hospital_admin(request):
    if bool(user_info) and user_info['type'] == 'hospital_admin':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_hospital_by_user(request):
    if bool(user_info) and user_info['type'] == 'user':
        return filter_search_hospital(request)
    else:
        return HttpResponse("No Access")


def filter_search_hospital(request):
    area = request.POST.get('select_area', 'No Preferences')

    statement = ""
    if area == "No Preferences":
        if user_info['type'] == "doctor":
            return redirect(search_hospitals_by_doctor)
        elif user_info['type'] == "user":
            return redirect(search_hospitals_by_users)
        elif user_info['type'] == "hospital_admin":
            return redirect(search_hospitals_by_hospitals)
        elif user_info['type'] == "blood_bank_admin":
            return redirect(search_hospitals_by_bloodbank)

    else:
        statement = "SELECT HOSPITAL_NAME,PHONE, LOCATION, HOSPITAL_ID FROM MEDI_SHEBA.HOSPITAL WHERE LOCATION = " + "\'" + area + "\'"

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    hospitalList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(statement)
    index = 1
    for row in c:
        hospitalList.append(HospitalName(index, row[0], row[1], row[2], row[3]))
        index = index + 1

    conn.close()
    if user_info['type'] == "doctor":
        return render(request, "query_pages/query_page_for_doctors/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "user":
        return render(request, "query_pages/query_page_for_users/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "hospital_admin":
        return render(request, "query_pages/query_page_for_hospital_admin/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "blood_bank_admin":
        return render(request, "query_pages/query_page_for_blood_bank_admin/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})


def search_hospitals_by_doctor(request):
    return see_hospitals(request)


def search_hospitals_by_users(request):
    return see_hospitals(request)


def search_hospitals_by_bloodbank(request):
    return see_hospitals(request)


def see_hospitals(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    hospitalList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT HOSPITAL_NAME,PHONE,LOCATION , HOSPITAL_ID from MEDI_SHEBA.HOSPITAL")
    index = 1
    for row in c:
        hospitalList.append(HospitalName(index, row[0], row[1], row[2], row[3]))  # HospitalName is defined in models.py
        index = index + 1
        '''print(row[2])'''
    conn.close()

    if user_info['type'] == "doctor":
        return render(request, "query_pages/query_page_for_doctors/hospital_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "user":
        return render(request, "query_pages/query_page_for_users/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "hospital_admin":
        return render(request, "query_pages/query_page_for_hospital_admin/hospital_custom_query.html",
                      {'hos': hospitalList, 'opt': location_names})
    elif user_info['type'] == "blood_bank_admin":
        return render(request, "query_pages/query_page_for_blood_bank_admin/hospital_query.html",
                      {'hos': hospitalList, 'opt': location_names})


# Blood_Bank

# Blood_Bank


# USER HOMEPAGE FUNCTIONS

def user_search_options(request):
    return render(request, 'homepage/Search_for_user.html')


def bloodbank_search_options(request):
    return render(request, 'homepage/Search_for_bloodbank.html')


def submit_changed_profile_user(request):
    first_name = request.POST['f_name']
    last_name = request.POST['l_name']
    phone_number = request.POST['phone']
    email = request.POST['email']
    blood_type = request.POST['blood_type']
    # bio = request.POST['additional_details']

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

    print(user_info['pk'])
    if first_name != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET FIRST_NAME = " + "\'" + first_name + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("First Name NOT CHANGED ")

    if last_name != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET LAST_NAME = " + "\'" + last_name + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("LAST Name NOT CHANGED ")

    if phone_number != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET PHONE = " + "\'" + phone_number + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("PHONE NOT CHANGED ")

    if email != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET EMAIL = " + "\'" + email + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("EMAIL NOT CHANGED ")

    if blood_type != "":
        c = conn.cursor()
        statement = "UPDATE MEDI_SHEBA.USERS SET BLOOD_GROUP = " + "\'" + blood_type + "\'" + "WHERE USER_ID = " + str(
            user_info['pk'])
        c.execute(statement)
        conn.commit()
    else:
        print("BLOOD NOT CHANGED ")

    '''
    UPDATE DICTIONARY HERE, CAUSE NOT UPDATING THE DICTIONARY WILL SHOW WRONG INFORMATION ON THE PAGES
    UPDATE EMAIL, FIRST NAME, LAST NAME
    '''

    '''
    TODO: HANDLE MULTI VALUE DICT KEY ERROR IF SOMETHING IS NOT GIVEN AS INPUT, SPECIALLY DROP DOWN BOXES 
    '''
    c = conn.cursor()
    statement = "SELECT USER_ID, FIRST_NAME, LAST_NAME,EMAIL from MEDI_SHEBA.USERS  WHERE USER_ID=" + str(
        user_info['pk'])
    c.execute(statement)
    if c:
        x = c.fetchone()
        id = x[0]
        f_name = x[1]
        l_name = x[2]
        email = x[3]
        user_info['pk'] = id
        user_info['f_name'] = f_name
        user_info['l_name'] = l_name
        user_info['email'] = email
    return redirect("user_home")


def user_edit_profile(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "user":
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
        c.execute(statement)

        hospital_names = []

        for i in c:
            hospital_names.append(i[0])

        location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
        location_names.sort()

        return render(request, 'profile_editor/UserProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def user_doctor_appointment(request):
    return render(request, 'appointment_history_pages/user_history/doctor/doctor_appointment_options.html')


# TODO: USER HISTORY
def past_appointment_of_doctor_by_user(request):
    if bool(user_info) and user_info['type'] == 'user':
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT D.DOCTOR_ID, D.FIRST_NAME, D.LAST_NAME, TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') FROM DOCTOR D,DOCTOR_USER_HISTORY DUH WHERE D.DOCTOR_ID = DUH.DOCTOR_ID AND DUH.USER_ID = " + str(
            user_info[
                'pk']) + " AND DUH.USER_TYPE = " + "\'" + "user" + "\'" + " AND TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') <= (SELECT TO_CHAR(SYSDATE,'yyyy-mm-dd') FROM DUAL)"

        c.execute(statement)
        past_appointment = []

        index = 1
        for r in c:
            past_appointment.append(doctor_user_history(index, user_info['pk'], r[0], r[1], r[2], r[3]))
            index = index + 1

        return render(request, 'appointment_history_pages/user_history/doctor/past_appointment_doctor.html',
                      {'past_appointment': past_appointment})
    else:
        return HttpResponse("NO ACCESS")


def check_users_prescription(request):
    if bool(user_info) and user_info['type'] == 'user':
        doctor_id = request.POST.get("doc_id", "None")
        user_id = user_info['pk']
        appointment_date = request.POST.get("appointment_time", "None")

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        patient_name = user_info['f_name'] + " " + user_info['l_name']
        patient_email = user_info['email']
        statement = "SELECT FIRST_NAME || ' ' || LAST_NAME, EMAIL FROM MEDI_SHEBA.DOCTOR WHERE DOCTOR_ID = " + str(
            doctor_id)
        c.execute(statement)
        doctor_name = ""
        doctor_email = ""
        for r in c:
            doctor_name = r[0]
            doctor_email = r[1]

        statement = "SELECT PROBLEM, PRESCRIPTION FROM MEDI_SHEBA.DOCTOR_USER_HISTORY WHERE USER_ID = " + str(
            user_id) + " AND DOCTOR_ID = " + str(
            doctor_id) + " AND TO_CHAR(APPOINTMENT_TIME,'yyyy-mm-dd') = " + "\'" + appointment_date + "\'"
        c.execute(statement)
        problem = ""
        prescription = ""

        for r in c:
            problem = r[0]
            prescription = r[1]

        return render(request, 'appointment_history_pages/user_history/doctor/show_problem_and_prescription.html',
                      {
                          'patient_name': patient_name,
                          'patient_email': patient_email,
                          'doctor_name': doctor_name,
                          'doctor_email': doctor_email,
                          'problem': problem,
                          'prescription': prescription
                      })
    else:
        return HttpResponse("NO ACCESS")


def upcoming_appointment_of_doctor_by_user(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT D.DOCTOR_ID, D.FIRST_NAME, D.LAST_NAME, TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') FROM DOCTOR D,DOCTOR_USER_HISTORY DUH WHERE D.DOCTOR_ID = DUH.DOCTOR_ID AND DUH.USER_ID = " + str(
        user_info[
            'pk']) + " AND DUH.USER_TYPE = " + "\'" + "user" + "\'" + " AND TO_CHAR(DUH.APPOINTMENT_TIME,'yyyy-mm-dd') > (SELECT TO_CHAR(SYSDATE,'yyyy-mm-dd') FROM DUAL)"

    c.execute(statement)
    upcoming_appointment = []

    index = 1
    for r in c:
        upcoming_appointment.append(doctor_user_history(index, user_info['pk'], r[0], r[1], r[2], r[3]))
        index = index + 1

    return render(request, 'appointment_history_pages/user_history/doctor/upcoming_appointment_doctor.html',
                  {'upcoming_appointment': upcoming_appointment})


def pending_appointment_of_doctor_by_user(request):
    return HttpResponse("Pending appointment")


def user_blood_bank_appointment(request):
    return render(request, 'appointment_history_pages/user_history/blood_bank/bloodbank_appointment_options.html')


def user_hospital_appointment(request):
    return render(request, 'appointment_history_pages/user_history/hospital/hospital_appointment_options.html')


def past_appointment_of_hospital_by_user(request):
    return HttpResponse("Past hospital appointment")


def upcoming_appointment_of_hospital_by_user(request):
    return HttpResponse("upcoming hospital appointment")


def pending_appointment_of_hospital_by_user(request):
    return HttpResponse("pending hospital appointment")


def past_appointment_of_bloodbank_by_user(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c2 = conn.cursor()
    done = "DONE"
    user_type = "user"
    statement = "SELECT USER_NAME,BLOOD_GROUP,AMOUNT,PENDING_STATUS,BLOOD_BANK_ID,USER_ID,USER_TYPE FROM MEDI_SHEBA.USER_BBANK_HISTORY WHERE USER_ID= " + str(
        user_info['pk']) + " AND PENDING_STATUS= " + "\'" + done + "\'" + "AND USER_TYPE=" + "\'" + user_type + "\'"
    c.execute(statement)
    conn.commit()
    blood_bank_name = []
    blood_bank_id = []
    user_details = []
    index = 1
    for i in c:
        blood_bank_id = i[4]
        statement = "SELECT NAME FROM BLOOD_BANK WHERE BLOOD_BANK_ID = " + str(blood_bank_id)
        c2.execute(statement)
        conn.commit()
        for row in c2:
            blood_bank_name.append(row[0])
            user_details.append(UserAppointment_in_blood_bank(index, row[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            index = index + 1
    conn.close()
    return render(request, 'appointment_history_pages/user_history/blood_bank/user_list_bloodbank_booking.html',
                  {'user_details': user_details, 'blood_bank_name': blood_bank_name})


def pending_appointment_of_bloodbank_by_user(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c2 = conn.cursor()
    done = "PENDING"
    user_type = "user"
    statement = "SELECT USER_NAME,BLOOD_GROUP,AMOUNT,PENDING_STATUS,BLOOD_BANK_ID,USER_ID,USER_TYPE FROM MEDI_SHEBA.USER_BBANK_HISTORY WHERE USER_ID= " + str(
        user_info['pk']) + " AND PENDING_STATUS= " + "\'" + done + "\'" + "AND USER_TYPE=" + "\'" + user_type + "\'"
    c.execute(statement)
    conn.commit()
    blood_bank_name = []
    blood_bank_id = []
    user_details = []
    index = 1
    for i in c:
        blood_bank_id = i[4]
        statement = "SELECT NAME FROM BLOOD_BANK WHERE BLOOD_BANK_ID = " + str(blood_bank_id)
        c2.execute(statement)
        conn.commit()
        for row in c2:
            blood_bank_name.append(row[0])
            user_details.append(UserAppointment_in_blood_bank(index, row[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            index = index + 1
    conn.close()
    return render(request, 'appointment_history_pages/user_history/blood_bank/user_list_bloodbank_booking.html',
                  {'user_details': user_details, 'blood_bank_name': blood_bank_name})


def pending_appointment_of_bloodbank_by_doctor(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c2 = conn.cursor()
    done = "PENDING"
    user_type = "doctor"
    statement = "SELECT USER_NAME,BLOOD_GROUP,AMOUNT,PENDING_STATUS,BLOOD_BANK_ID,USER_ID,USER_TYPE FROM MEDI_SHEBA.USER_BBANK_HISTORY WHERE USER_ID= " + str(
        user_info['pk']) + " AND PENDING_STATUS= " + "\'" + done + "\'" + "AND USER_TYPE=" + "\'" + user_type + "\'"
    c.execute(statement)
    conn.commit()
    blood_bank_name = []
    blood_bank_id = []
    user_details = []
    index = 1
    for i in c:
        blood_bank_id = i[4]
        statement = "SELECT NAME FROM BLOOD_BANK WHERE BLOOD_BANK_ID = " + str(blood_bank_id)
        c2.execute(statement)
        conn.commit()
        for row in c2:
            blood_bank_name.append(row[0])
            user_details.append(UserAppointment_in_blood_bank(index, row[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            index = index + 1
    conn.close()
    return render(request, 'appointment_history_pages/doctor_history/blood_bank/doclist_bloodbank_booking.html',
                  {'user_details': user_details, 'blood_bank_name': blood_bank_name})


def past_appointment_of_bloodbank_by_doctor(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c2 = conn.cursor()
    done = "DONE"
    user_type = "doctor"
    statement = "SELECT USER_NAME,BLOOD_GROUP,AMOUNT,PENDING_STATUS,BLOOD_BANK_ID,USER_ID,USER_TYPE FROM MEDI_SHEBA.USER_BBANK_HISTORY WHERE USER_ID= " + str(
        user_info['pk']) + " AND PENDING_STATUS= " + "\'" + done + "\'" + "AND USER_TYPE=" + "\'" + user_type + "\'"
    c.execute(statement)
    conn.commit()
    blood_bank_name = []
    blood_bank_id = []
    user_details = []
    index = 1
    for i in c:
        blood_bank_id = i[4]
        statement = "SELECT NAME FROM BLOOD_BANK WHERE BLOOD_BANK_ID = " + str(blood_bank_id)
        c2.execute(statement)
        conn.commit()
        for row in c2:
            blood_bank_name.append(row[0])
            user_details.append(UserAppointment_in_blood_bank(index, row[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            index = index + 1
    conn.close()
    return render(request, 'appointment_history_pages/doctor_history/blood_bank/doclist_bloodbank_booking.html',
                  {'user_details': user_details, 'blood_bank_name': blood_bank_name})


def user_modify_appointment(request):
    return HttpResponse("user modify appointment")


# BLOOD BANK ADMIN
def submit_changed_blood_group_collection(request):
    # print("ass")
    if bool(user_info) and user_info['type'] == 'blood_bank_admin':
        a_pos = request.POST['a_pos']
        a_neg = request.POST['a_neg']
        b_pos = request.POST['b_pos']
        b_neg = request.POST['b_neg']
        ab_pos = request.POST['ab_pos']
        ab_neg = request.POST['ab_neg']
        o_pos = request.POST['o_pos']
        o_neg = request.POST['o_neg']
        # print(a_pos)
        # print(o_neg)
        # print("asd")
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        if a_pos != "":
            # c = conn.cursor()
            # statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET A_POS = " + "\'" + a_pos + "\'" + "WHERE BLOOD_BANK_ID = " + str(user_info['pk'])
            # c.execute(statement)
            # conn.commit()

            # TODO: 1. PROCEDURE HERE for update
            c = conn.cursor()
            data = [user_info['pk'], a_pos]
            c.callproc('update_a_pos_blood', data)


        else:
            print("First Name NOT CHANGED ")

        if a_neg != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET A_NEG = " + "\'" + a_neg + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if b_pos != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET B_POS = " + "\'" + b_pos + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if b_neg != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET B_NEG = " + "\'" + b_neg + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if ab_pos != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET AB_POS = " + "\'" + ab_pos + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if ab_neg != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET AB_NEG = " + "\'" + ab_neg + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if o_pos != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET O_POS = " + "\'" + o_pos + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if o_neg != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET O_NEG = " + "\'" + o_neg + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")
        return redirect("blood_bank_admin_home")
    else:
        return HttpResponse("Access not granted")


def blood_bank_admin_edit_blood_group(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "blood_bank_admin":
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
        c.execute(statement)

        hospital_names = []

        for i in c:
            hospital_names.append(i[0])

        location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
        location_names.sort()

        return render(request, 'profile_editor/BloodBankAdminEditBG.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def bloodbank_admin_edit_profile(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "blood_bank_admin":
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
        c.execute(statement)

        hospital_names = []

        for i in c:
            hospital_names.append(i[0])

        location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
        location_names.sort()

        return render(request, 'profile_editor/BloodBankAdminProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def submit_changed_profile_bloodbank(request):
    if bool(user_info) and user_info['type'] == 'blood_bank_admin':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        phone_number = request.POST['phone']
        location = request.POST['address']
        email = request.POST['email']
        # blood_type = request.POST['blood_type']
        name = request.POST['name']
        # fee = request.POST['fee']
        # specialization = request.POST['specialization']
        # additional_details = request.POST['additional_details']

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

        if first_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET FIRST_NAME = " + "\'" + first_name + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if last_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET LAST_NAME = " + "\'" + last_name + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LAST Name NOT CHANGED ")

        if phone_number != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET PHONE = " + "\'" + phone_number + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("PHONE NOT CHANGED ")

        if location != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET LOCATION = " + "\'" + location + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LOCATION NOT CHANGED ")

        if email != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET EMAIL = " + "\'" + email + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("EMAIL NOT CHANGED ")

        if name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET NAME = " + "\'" + name + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()

        else:
            print("EMAIL NOT CHANGED ")

        c = conn.cursor()
        statement = "SELECT BLOOD_BANK_ID, FIRST_NAME, LAST_NAME,EMAIL from MEDI_SHEBA.BLOOD_BANK  WHERE BLOOD_BANK_ID=" + str(
            user_info['pk'])
        c.execute(statement)
        if c:
            x = c.fetchone()
            id = x[0]
            f_name = x[1]
            l_name = x[2]
            email = x[3]
            user_info['pk'] = id
            user_info['f_name'] = f_name
            user_info['l_name'] = l_name
            user_info['email'] = email
        return redirect("blood_bank_admin_home")
    else:
        return HttpResponse("Access not granted")


def bloodbank_collection(request):
    blood_bank_id = user_info['pk']
    # hospital_id_for_doctor = hospital_id
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    print(blood_bank_id)
    c.execute(
        "SELECT NAME, PHONE, LOCATION, EMAIL,A_POS,A_NEG,B_POS,B_NEG,AB_POS,AB_NEG,O_POS,O_NEG FROM MEDI_SHEBA.BLOOD_BANK WHERE BLOOD_BANK_ID = " + str(
            blood_bank_id))

    blood_bank_name = ""
    phone = ""
    location = ""
    email = ""
    a_pos = ""
    a_neg = ""
    b_pos = ""
    b_neg = ""
    ab_pos = ""
    ab_neg = ""
    o_pos = ""
    o_neg = " "

    for row in c:
        blood_bank_name = row[0]
        phone = row[1]
        location = row[2]
        email = row[3]
        a_pos = row[4]
        a_neg = row[5]
        b_pos = row[6]
        b_neg = row[7]
        ab_pos = row[8]
        ab_neg = row[9]
        o_pos = row[10]
        o_neg = row[11]

    return render(request, "detail_showing_pages/see_bloodbank_collection.html",
                  {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                   'phone': phone, 'location': location, 'email': email,
                   'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                   'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg,
                   })


def bloodbank_calender(request):
    return HttpResponse("etate kaaj kora lagbe")


def bloodbank_history(request):
    return HttpResponse("etate kaaj kora lagbe")


def bloodbank_all_appointments(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT USER_NAME,BLOOD_GROUP,AMOUNT,PENDING_STATUS,BLOOD_BANK_ID,USER_ID,USER_TYPE FROM MEDI_SHEBA.USER_BBANK_HISTORY WHERE BLOOD_BANK_ID= " + str(
        user_info['pk'])
    c.execute(statement)
    conn.commit()
    user_details = []
    index = 1
    for i in c:
        user_details.append(UserAppointment_in_blood_bank(index, i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        index = index + 1
    conn.close()
    return render(request, 'bloodbank_tables/approval_table.html', {'user_details': user_details})


def bloodbank_pending_status_changed(request):
    blood_bank_id = request.POST['blood_bank_id']
    user_id = request.POST['user_id']
    amount = request.POST['amount']
    blood_group = request.POST['blood_group']
    DONE = "DONE"
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "UPDATE MEDI_SHEBA.USER_BBANK_HISTORY SET PENDING_STATUS = " + "\'" + DONE + "\'" + "WHERE USER_ID = " + str(
        user_id) + " AND BLOOD_BANK_ID = " + str(
        blood_bank_id) + " AND AMOUNT = " + amount + " AND BLOOD_GROUP =" + "\'" + blood_group + "\'"

    c.execute(statement)
    conn.commit()

    statement = "SELECT USER_NAME,BLOOD_GROUP,AMOUNT,PENDING_STATUS,BLOOD_BANK_ID,USER_ID,USER_TYPE FROM MEDI_SHEBA.USER_BBANK_HISTORY WHERE BLOOD_BANK_ID= " + str(
        user_info['pk'])
    c.execute(statement)
    conn.commit()
    user_details = []
    index = 1
    for i in c:
        user_details.append(UserAppointment_in_blood_bank(index, i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        index = index + 1
    conn.close()
    return render(request, 'bloodbank_tables/approval_table.html', {'user_details': user_details})


# functions for hospital admin and management


def hospital_search_options(request):
    return render(request, 'homepage/search_for_hospitals.html')


def hospital_admin_edit_profile(request):
    # authentication added here
    if bool(user_info) and user_info['type'] == "hospital_admin":
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL"
        c.execute(statement)

        hospital_names = []

        for i in c:
            hospital_names.append(i[0])

        location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
        location_names.sort()

        return render(request, 'profile_editor/HospitalProfileEditor.html',
                      {'hospital_names': hospital_names, 'locations': location_names})

    else:
        return HttpResponse("NO ACCESS TO THIS PAGE")


def submit_changed_profile_hospital(request):
    if bool(user_info) and user_info['type'] == 'hospital_admin':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        phone_number = request.POST['phone']
        location = request.POST['address']
        email = request.POST['email']
        # blood_type = request.POST['blood_type']
        # hospital_name = request.POST['hospital_name']
        # fee = request.POST['fee']
        # specialization = request.POST['specialization']
        # additional_details = request.POST['additional_details']

        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)

        if first_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET FIRST_NAME = " + "\'" + first_name + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("First Name NOT CHANGED ")

        if last_name != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET LAST_NAME = " + "\'" + last_name + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LAST Name NOT CHANGED ")

        if phone_number != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET PHONE = " + "\'" + phone_number + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("PHONE NOT CHANGED ")

        if location != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET LOCATION = " + "\'" + location + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("LOCATION NOT CHANGED ")

        if email != "":
            c = conn.cursor()
            statement = "UPDATE MEDI_SHEBA.HOSPITAL SET EMAIL = " + "\'" + email + "\'" + "WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement)
            conn.commit()
        else:
            print("EMAIL NOT CHANGED ")

        '''
        TODO: HANDLE MULTI VALUE DICT KEY ERROR IF SOMETHING IS NOT GIVEN AS INPUT, SPECIALLY DROP DOWN BOXES 
        '''
        c = conn.cursor()
        statement = "SELECT HOSPITAL_ID, FIRST_NAME, LAST_NAME,EMAIL from MEDI_SHEBA.HOSPITAL  WHERE HOSPITAL_ID=" + str(
            user_info['pk'])
        c.execute(statement)
        if c:
            x = c.fetchone()
            id = x[0]
            f_name = x[1]
            l_name = x[2]
            email = x[3]
            user_info['pk'] = id
            user_info['f_name'] = f_name
            user_info['l_name'] = l_name
            user_info['email'] = email
        return redirect("hospital_admin_home")
    else:
        return HttpResponse("Access not granted")


# TODO: CABIN MANAGEMENT BY HOSPITAL ADMIN
def hospital_admin_cabin_management(request):
    return render(request, 'cabin/cabin_front_page.html')


def add_cabin_to_hospital(request):
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT HOSPITAL_NAME FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_ID = " + str(user_info['pk'])
    c.execute(statement)
    hospital_name = ""
    for row in c:
        hospital_name = row[0]

    return render(request, 'cabin/cabin_add.html', {'hospital_name': hospital_name})


def add_cabin_to_hospital_form_submission(request):
    if bool(user_info) and user_info['type'] == 'hospital_admin':
        price = request.POST.get('price', 'Not Specified')
        category = request.POST.get('category', 'Not Specified')
        cabin_features = request.POST.get('cabin_features', 'Not Specified')

        if price == "Not Specified" or category == "Not Specified" or cabin_features == "Not Specified":
            return redirect("add_cabin_to_hospital")

        else:
            dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
            conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
            c = conn.cursor()
            statement = "INSERT INTO MEDI_SHEBA.CABIN(PRICE, CATEGORY, HOSPITAL_ID,CABIN_FEATURES) VALUES (" + str(
                price) + "," + "\'" + category + "\'," + str(user_info['pk']) + "," + "\'" + cabin_features + "\')"
            c.execute(statement)
            conn.commit()

            prev_cabin_count = 0
            statement2 = "SELECT NVL(AVAILABLE_CABIN,0) FROM MEDI_SHEBA.HOSPITAL WHERE HOSPITAL_ID = " + str(
                user_info['pk'])
            c.execute(statement2)
            for row in c:
                prev_cabin_count = row[0]
            prev_cabin_count = prev_cabin_count + 1

            # statement3 = "UPDATE MEDI_SHEBA.HOSPITAL SET AVAILABLE_CABIN = " + str(prev_cabin_count) + " WHERE HOSPITAL_ID = " + str(user_info['pk'])
            # c.execute(statement3)
            # conn.commit()

            # TODO : PROCEDURE IN HOSPITAL CABIN ADD
            c = conn.cursor()
            data = [user_info['pk'], prev_cabin_count]
            c.callproc('update_cabin_count_in_hospital', data)

            return render(request, 'cabin/cabin_add_confirmation.html')
    return HttpResponse("NO ACCESS")


def go_to_hospital_admin_home(request):
    return redirect("hospital_admin_home")


def check_cabin_history(request):
    usercabinList = []
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "select CU.CABIN_ID,CU.USER_ID,H.HOSPITAL_NAME,TO_CHAR(CU.ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(CU.EXIT_DATE,'yyyy-mm-dd'),CU.USER_TYPE from MEDI_SHEBA.CABIN_USER_APPOINTMENT CU JOIN MEDI_SHEBA.HOSPITAL H ON CU.CABIN_ID in (SELECT C.CABIN_ID FROM MEDI_SHEBA.CABIN C where C.HOSPITAL_ID=H.HOSPITAL_ID) and CU.EXIT_DATE<SYSDATE and H.HOSPITAL_ID= " + str(
        user_info['pk'])
    c.execute(statement)
    index = 1
    for row in c:
        usercabinList.append(userCabinHistory(index, row[0], row[1], row[2], row[3], row[4], row[5]))
    index = index + 1
    conn.close()
    return render(request, "cabin/cabin_history.html", {'uch': usercabinList})


def check_occupied_cabin(request):
    usercabinList = []
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "select CU.CABIN_ID,CU.USER_ID,H.HOSPITAL_NAME,TO_CHAR(CU.ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(CU.EXIT_DATE,'yyyy-mm-dd'),CU.USER_TYPE from MEDI_SHEBA.CABIN_USER_APPOINTMENT CU JOIN MEDI_SHEBA.HOSPITAL H ON CU.CABIN_ID in (SELECT C.CABIN_ID FROM MEDI_SHEBA.CABIN C where C.HOSPITAL_ID=H.HOSPITAL_ID) and CU.ENTRY_DATE<=SYSDATE and CU.EXIT_DATE>=SYSDATE and H.HOSPITAL_ID= " + str(
        user_info['pk'])
    c.execute(statement)
    index = 1
    for row in c:
        usercabinList.append(userCabinHistory(index, row[0], row[1], row[2], row[3], row[4], row[5]))
    index = index + 1
    conn.close()
    return render(request, "cabin/cabin_occupied.html", {'uch': usercabinList})


def check_cabin_pending_appointments(request):
    usercabinList = []
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "select CU.CABIN_ID,CU.USER_ID,H.HOSPITAL_NAME,TO_CHAR(CU.ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(CU.EXIT_DATE,'yyyy-mm-dd'),CU.USER_TYPE from MEDI_SHEBA.CABIN_USER_APPOINTMENT CU JOIN MEDI_SHEBA.HOSPITAL H ON CU.CABIN_ID in (SELECT C.CABIN_ID FROM MEDI_SHEBA.CABIN C where C.HOSPITAL_ID=H.HOSPITAL_ID) and CU.ENTRY_DATE>SYSDATE and H.HOSPITAL_ID= " + str(
        user_info['pk'])
    c.execute(statement)
    index = 1
    for row in c:
        usercabinList.append(userCabinHistory(index, row[0], row[1], row[2], row[3], row[4], row[5]))
    index = index + 1
    conn.close()
    return render(request, "cabin/cabin_pending_appointments.html", {'uch': usercabinList})


def hospital_admin_view_records(request):
    return HttpResponse("Hospital admin view records")


def search_doctors_by_hospitals(request):
    return see_doctors(request)


def search_hospitals_by_hospitals(request):
    return see_hospitals(request)


# blood banks custom search

def see_blood_banks(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    bbankList = []
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    '''
    c.execute("SELECT NAME,'A+','A-','B+','B-','O+','O-','AB+','AB-'"
              "from MEDI_SHEBA.BLOOD_BANK")
    '''

    statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK"
    c.execute(statement)

    index = 1
    for row in c:
        bbankList.append(
            BloodBankList(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                          row[10]))
        index = index + 1
    conn.close()
    if user_info['type'] == 'doctor':
        return render(request, "query_pages/query_page_for_doctors/bb_query.html",
                      {'b_banks': bbankList, 'opt': location_names})
    elif user_info['type'] == 'user':
        return render(request, "query_pages/query_page_for_users/bb_query.html",
                      {'b_banks': bbankList, 'opt': location_names})
    elif user_info['type'] == 'blood_bank_admin':
        return render(request, "query_pages/query_page_for_blood_bank_admin/bb_query.html",
                      {'b_banks': bbankList, 'opt': location_names})
    elif user_info['type'] == "hospital_admin":
        return render(request, "query_pages/query_page_for_hospital_admin/bb_custom_query.html",
                      {'b_banks': bbankList, 'opt': location_names})


def see_specific_bloodbank_details(request):
    blood_bank_id = request.POST['blood_bank_id']
    # hospital_id_for_doctor = hospital_id
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c2 = conn.cursor()
    print(blood_bank_id)

    statement = ""

    c.execute(
        "SELECT NAME, PHONE, LOCATION, EMAIL,A_POS,A_NEG,B_POS,B_NEG,AB_POS,AB_NEG,O_POS,O_NEG FROM MEDI_SHEBA.BLOOD_BANK WHERE BLOOD_BANK_ID = " + str(
            blood_bank_id))

    blood_bank_name = ""
    phone = ""
    location = ""
    email = ""
    a_pos = ""
    a_neg = ""
    b_pos = ""
    b_neg = ""
    ab_pos = ""
    ab_neg = ""
    o_pos = ""
    o_neg = " "

    for row in c:
        blood_bank_name = row[0]
        phone = row[1]
        location = row[2]
        email = row[3]
        a_pos = row[4]
        a_neg = row[5]
        b_pos = row[6]
        b_neg = row[7]
        ab_pos = row[8]
        ab_neg = row[9]
        o_pos = row[10]
        o_neg = row[11]
    msg = ""

    return render(request, "detail_showing_pages/see_bloodbank_details.html",
                  {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                   'phone': phone, 'location': location, 'email': email,
                   'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                   'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                   })


def search_blood_banks_by_hospital_admin(request):
    return see_blood_banks(request)


def search_blood_banks_by_doctor(request):
    return see_blood_banks(request)


def search_blood_banks_by_user(request):
    return see_blood_banks(request)


def search_blood_banks_by_bloodbank(request):
    return see_blood_banks(request)


def custom_search_for_bloodbank_by_doctor(request):
    if bool(user_info) and user_info['type'] == 'doctor':
        return filter_search_bloodbank(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_bloodbank_by_user(request):
    if bool(user_info) and user_info['type'] == 'user':
        return filter_search_bloodbank(request)
    else:
        return HttpResponse("No Access")


def custom_search_for_bloodbank_by_blood_bank_admin(request):
    if bool(user_info) and user_info['type'] == 'blood_bank_admin':
        return filter_search_bloodbank(request)
    else:
        return HttpResponse("NO ACCESS")


def custom_search_for_bloodbank_by_hospital_admin(request):
    if bool(user_info) and user_info['type'] == 'hospital_admin':
        return filter_search_bloodbank(request)
    else:
        return HttpResponse("No Access")


def submit_blood_bank_appointment(request):
    name = user_info['f_name'] + " " + user_info['l_name']
    blood_group = request.POST.get('blood_group', 'No preference')
    amount = request.POST.get('amount', 'No preference')
    blood_bank_id = request.POST.get('blood_bank_id', 'No preference')
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT NAME, PHONE, LOCATION, EMAIL,A_POS,A_NEG,B_POS,B_NEG,AB_POS,AB_NEG,O_POS,O_NEG FROM MEDI_SHEBA.BLOOD_BANK WHERE BLOOD_BANK_ID = " + str(
        blood_bank_id)
    pending_status = "PENDING"
    c.execute(statement)
    conn.commit()
    statement2 = "INSERT INTO MEDI_SHEBA.USER_BBANK_HISTORY(BLOOD_BANK_ID,USER_ID,USER_NAME,BLOOD_GROUP,AMOUNT,PENDING_STATUS,USER_TYPE) " \
                 "VALUES" \
                 " (" + "\'" + str(blood_bank_id) + "\'," + "\'" + str(
        user_info[
            'pk']) + "\'," + "\'" + name + "\'," + "\'" + blood_group + "\'," + "\'" + amount + "\'," + "\'" + pending_status + "\'," + "\'" + \
                 user_info['type'] + "\'" + ")"
    blood_bank_name = ""
    phone = ""
    location = ""
    email = ""
    a_pos = ""
    a_neg = ""
    b_pos = ""
    b_neg = ""
    ab_pos = ""
    ab_neg = ""
    o_pos = ""
    o_neg = " "
    for row in c:
        blood_bank_name = row[0]
        phone = row[1]
        location = row[2]
        email = row[3]
        a_pos = row[4]
        a_neg = row[5]
        b_pos = row[6]
        b_neg = row[7]
        ab_pos = row[8]
        ab_neg = row[9]
        o_pos = row[10]
        o_neg = row[11]
    if blood_group == "A+":
        if int(amount) > a_pos:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET A_POS =  " + "\'" + str(
                a_pos - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()

            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})
    elif blood_group == "A-":
        if int(amount) > a_neg:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET A_NEG = " + "\'" + str(
                a_neg - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()
            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})
    elif blood_group == "B+":
        if int(amount) > b_pos:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET B_POS = " + "\'" + str(
                b_pos - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()
            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})
    elif blood_group == "B-":
        if int(amount) > b_neg:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET B_NEG = " + "\'" + str(
                b_neg - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()
            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})
    elif blood_group == "AB+":
        if int(amount) > ab_pos:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET AB_POS = " + "\'" + str(
                ab_pos - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()
            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})
    elif blood_group == "AB-":
        if int(amount) > ab_neg:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET AB_NEG = " + "\'" + str(
                ab_neg - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()
            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})
    elif blood_group == "O+":
        if int(amount) > o_pos:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET O_POS = " + "\'" + str(
                o_pos - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()
            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})
    elif blood_group == "O-":
        if int(amount) > o_neg:
            msg = "Invalid Amount"
            return render(request, "detail_showing_pages/see_bloodbank_details.html",
                          {'blood_bank_id': blood_bank_id, 'name': blood_bank_name,
                           'phone': phone, 'location': location, 'email': email,
                           'a_pos': a_pos, 'a_neg': a_neg, 'ab_pos': ab_pos, 'ab_neg': ab_neg,
                           'b_pos': b_pos, 'b_neg': b_neg, 'o_pos': o_pos, 'o_neg': o_neg, 'msg': msg,
                           })
        else:
            if user_info['type'] == 'user':
                c.execute(statement2)
                conn.commit()
            elif user_info['type'] == 'doctor':
                c.execute(statement2)
                conn.commit()
            statement = "UPDATE MEDI_SHEBA.BLOOD_BANK SET O_NEG = " + "\'" + str(
                o_neg - int(amount)) + "\'" + "WHERE BLOOD_BANK_ID = " + str(
                blood_bank_id)
            c.execute(statement)
            conn.commit()
            return render(request, "appointment_history_pages/blood_bank_history/appointment_confirmed.html",
                          {'blood_group': blood_group, 'amount': amount})


def filter_search_bloodbank(request):
    area = request.POST.get('select_area', 'No Preferences')
    blood_group = request.POST.get('blood_group', 'No Preferences')

    blood_type_db = ""
    if blood_group == "A+":
        blood_type_db = "A_POS"
    elif blood_group == "A-":
        blood_type_db = "A_NEG"
    elif blood_group == "B+":
        blood_type_db = "B_POS"
    elif blood_group == "B-":
        blood_type_db = "B_NEG"
    elif blood_group == "O+":
        blood_type_db = "O_POS"
    elif blood_group == "O-":
        blood_type_db = "O_NEG"
    elif blood_group == "AB+":
        blood_type_db = "AB_POS"
    elif blood_group == "AB-":
        blood_type_db = "AB_NEG"

    statement = ""
    if area == "No Preferences" and blood_group == "No Preferences":
        if user_info['type'] == "doctor":
            return redirect(search_blood_banks_by_doctor)
        elif user_info['type'] == "user":
            return redirect(search_blood_banks_by_user)
        elif user_info['type'] == "hospital_admin":
            return redirect(search_blood_banks_by_hospital_admin)
        elif user_info['type'] == "blood_bank_admin":
            return redirect(search_blood_banks_by_bloodbank)

    else:
        if blood_group == "No Preferences":
            statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK WHERE LOCATION = " + "\'" + area + "\'"

        elif area == "No Preferences":

            statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK ORDER BY  " + blood_type_db + " DESC NULLS LAST"

        else:
            statement = "SELECT NAME, A_POS, A_NEG, B_POS, B_NEG, O_POS, O_NEG, AB_POS, AB_NEG,BLOOD_BANK_ID,LOCATION FROM MEDI_SHEBA.BLOOD_BANK WHERE LOCATION = " + "\'" + area + "\'" + " ORDER BY  " + blood_type_db + " DESC NULLS LAST"

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    bbList = []
    # print(blood_group)
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(statement)
    index = 1
    for row in c:
        bbList.append(
            BloodBankList(index, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                          row[10]))
        index = index + 1

    conn.close()

    statement = ""
    if user_info['type'] == "doctor":
        return render(request, "query_pages/query_page_for_doctors/bb_custom_query.html",
                      {'b_banks': bbList, 'opt': location_names})
    elif user_info['type'] == "user":
        return render(request, "query_pages/query_page_for_users/bb_custom_query.html",
                      {'b_banks': bbList, 'opt': location_names})

    elif user_info['type'] == "hospital_admin":
        return render(request, "query_pages/query_page_for_hospital_admin/bb_custom_query.html",
                      {'b_banks': bbList, 'opt': location_names})

    elif user_info['type'] == "blood_bank_admin":
        return render(request, "query_pages/query_page_for_blood_bank_admin/bb_custom_query.html",
                      {'b_banks': bbList, 'opt': location_names})


'''
  cabin starts
'''

'''
  cabin search for doctors
'''


def search_cabin_by_doctor(request):
    return see_hospital_cabins(request)


def custom_search_for_cabin_by_doctor(request):
    return filter_search_cabin(request)


def filter_search_cabin(request):
    area = request.POST.get('select_area', 'No Preferences')
    statement = ""
    if area == "No Preferences":
        statement = "SELECT HOSPITAL_NAME, LOCATION ,AVAILABLE_CABIN , HOSPITAL_ID FROM MEDI_SHEBA.HOSPITAL"
    else:
        statement = "SELECT HOSPITAL_NAME, LOCATION ,AVAILABLE_CABIN , HOSPITAL_ID FROM MEDI_SHEBA.HOSPITAL WHERE LOCATION = " + "\'" + area + "\'"

    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()
    hospitalcabinList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute(statement)
    index = 1
    for row in c:
        hospitalcabinList.append(HospitalCabinName(index, row[0], row[1], row[2], row[3]))
        index = index + 1
    conn.close()
    if user_info['type'] == 'doctor':
        return render(request, "query_pages/query_page_for_doctors/cabin_custom_query_by_doctor.html",
                      {'cab': hospitalcabinList, 'opt': location_names})
    else:
        return render(request, "query_pages/query_page_for_users/cabin_custom_query_by_user.html",
                      {'cab': hospitalcabinList, 'opt': location_names})


def see_hospital_cabins(request):
    location_names = json_extractor.JsonExtractor('name').extract("HelperClasses/zilla_names.json")
    location_names.sort()

    hospitalcabinList = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    c.execute("SELECT HOSPITAL_NAME, LOCATION ,AVAILABLE_CABIN , HOSPITAL_ID from MEDI_SHEBA.HOSPITAL")
    index = 1
    for row in c:
        hospitalcabinList.append(HospitalCabinName(index, row[0], row[1], row[2], row[3]))
        index = index + 1

    conn.close()
    if user_info['type'] == 'doctor':
        return render(request, "query_pages/query_page_for_doctors/cabin_query_by_doctor.html",
                      {'cab': hospitalcabinList, 'opt': location_names})
    else:
        return render(request, "query_pages/query_page_for_users/cabin_query_by_user.html",
                      {'cab': hospitalcabinList, 'opt': location_names})


def see_specific_hospital_cabin_details(request):
    hospital_id = request.POST['hospital_id']
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    cabinList = []
    c.execute(
        "SELECT PRICE, CATEGORY,CABIN_ID, HOSPITAL_ID FROM MEDI_SHEBA.CABIN WHERE HOSPITAL_ID = " + str(
            hospital_id))

    index = 1
    for row in c:
        cabinList.append(CabinName(index, row[0], row[1], row[2]))
        index = index + 1
    conn.close()
    if user_info['type'] == 'doctor':
        return render(request, "detail_showing_pages/hospital_cabin_details_by_doctor.html",
                      {'cab': cabinList})
    else:
        return render(request, "detail_showing_pages/hospital_cabin_details_by_user.html",
                      {'cab': cabinList})


def book_cabin_by_doctor(request):
    cabin_id = request.POST['cabin_id']
    cabin_id_for_doctor = cabin_id
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    c.execute(
        "SELECT H.HOSPITAL_NAME, C.CATEGORY, C.PRICE, C.CABIN_ID FROM MEDI_SHEBA.CABIN C join MEDI_SHEBA.HOSPITAL H On C.HOSPITAL_ID=H.HOSPITAL_ID WHERE C.CABIN_ID = " + str(
            cabin_id))

    hospital_name = ""
    category = ""
    price = ""
    cabin_id_for_doctor = ""

    for row in c:
        hospital_name = row[0]
        category = row[1]
        price = row[2]
        cabin_id_for_doctor = row[3]

    return render(request, "cabin/cabin_booking_by_doctor.html",
                  {'name': hospital_name,
                   'category': category, 'price': price,
                   'cabin_id_for_doctor': cabin_id_for_doctor
                   })


def check_cabin_availability_by_doctor(request):
    inputed_entry_date = request.GET['entrydate']
    inputed_exit_date = request.GET['exitdate']
    cabin_id = request.GET['cabin_id_for_doctor']
    list_of_dates = []

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    statement = "SELECT TO_CHAR(ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(EXIT_DATE,'yyyy-mm-dd') FROM MEDI_SHEBA.CABIN_USER_APPOINTMENT WHERE CABIN_ID = " + str(
        cabin_id)
    c.execute(statement)

    for r in c:
        list_of_dates.append(r[0])
        list_of_dates.append(r[1])

    serial_dates = []
    for x in range(0, len(list_of_dates), 2):
        return_list = sequential_date_generator.FindSequenceOfDays(list_of_dates[x],
                                                                   list_of_dates[x + 1]).generate_sequence()
        for ss in return_list:
            serial_dates.append(ss.strftime('%Y-%m-%d'))
    '''
    for x in serial_dates:
        print(x)
    '''
    f = 0
    for x in serial_dates:
        if x == inputed_entry_date or x == inputed_exit_date:
            f = 1
            break
        elif inputed_entry_date < x and inputed_exit_date > x:
            f = 1
            break
    if f == 1:
        cabinBookingList = []
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT CABIN_ID,TO_CHAR(ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(EXIT_DATE,'yyyy-mm-dd') from CABIN_USER_APPOINTMENT where CABIN_ID = " + str(
            cabin_id)
        c.execute(statement)
        index = 1
        for row in c:
            cabinBookingList.append(cabinBookingDetails(index, row[0], row[1], row[2]))
            index = index + 1
        conn.close()
        return render(request, "cabin/cabin_booking_error_page_by_doctor.html",
                      {'uch': cabinBookingList, 'cabin_id': request.GET['cabin_id_for_doctor']})
    else:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO MEDI_SHEBA.CABIN_USER_APPOINTMENT(USER_ID,CABIN_ID,ENTRY_DATE,EXIT_DATE,USER_TYPE) " \
                    "VALUES" \
                    " (" + "\'" + str(user_info['pk']) + "\'," + "\'" + str(
            cabin_id) + "\'," + "TO_DATE(" + "\'" + inputed_entry_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," \
                    + "TO_DATE(" + "\'" + inputed_exit_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + \
                    user_info['type'] + "\'" + ")"
        c.execute(statement)
        conn.commit()
        return redirect("submit_book_cabin_by_doctor")


def submit_book_cabin_by_doctor(request):
    return render(request, "cabin/cabin_booking_confirmation_by_doctor.html")


def go_to_doctor_home(request):
    return redirect("doctor_home")


def cabin_booking_history_by_doctor(request):
    cabinBookingList = []
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT USER_ID,CABIN_ID,TO_CHAR(ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(EXIT_DATE,'yyyy-mm-dd'),USER_TYPE from CABIN_USER_APPOINTMENT where USER_ID= " + str(
        user_info['pk']) + " AND USER_TYPE = " + "\'" + user_info['type'] + "\'"
    c.execute(statement)
    print(statement)
    index = 1
    for row in c:
        cabinBookingList.append(cabinBookingHistory(index, row[0], row[1], row[2], row[3], row[4]))
        index = index + 1
    conn.close()
    return render(request, "cabin/cabin_booking_history_by_doctor.html", {'cbh': cabinBookingList})


'''
  cabin search for users
'''


def search_cabin_by_user(request):
    return see_hospital_cabins(request)


def custom_search_for_cabin_by_user(request):
    return filter_search_cabin(request)


def book_cabin_by_user(request):
    cabin_id = request.POST['cabin_id']
    cabin_id_for_user = cabin_id
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    c.execute(
        "SELECT H.HOSPITAL_NAME, C.CATEGORY, C.PRICE, C.CABIN_ID FROM MEDI_SHEBA.CABIN C join MEDI_SHEBA.HOSPITAL H On C.HOSPITAL_ID=H.HOSPITAL_ID WHERE C.CABIN_ID = " + str(
            cabin_id))

    hospital_name = ""
    category = ""
    price = ""
    cabin_id_for_user = ""

    for row in c:
        hospital_name = row[0]
        category = row[1]
        price = row[2]
        cabin_id_for_user = row[3]

    return render(request, "cabin/cabin_booking_by_user.html",
                  {'name': hospital_name,
                   'category': category, 'price': price,
                   'cabin_id_for_user': cabin_id_for_user,
                   })


def check_cabin_availability_by_user(request):
    inputed_entry_date = request.GET['entrydate']
    inputed_exit_date = request.GET['exitdate']
    cabin_id = request.GET['cabin_id_for_user']
    list_of_dates = []
    #  TO_CHAR(APPOINTMENT_DATE,'yyyy-mm-dd')

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    statement = "SELECT TO_CHAR(ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(EXIT_DATE,'yyyy-mm-dd') FROM MEDI_SHEBA.CABIN_USER_APPOINTMENT WHERE CABIN_ID = " + str(
        cabin_id)
    c.execute(statement)

    for r in c:
        list_of_dates.append(r[0])
        list_of_dates.append(r[1])

    serial_dates = []
    # day = day_name.FindDayName(selected_date).find_day_name()
    for x in range(0, len(list_of_dates), 2):
        return_list = sequential_date_generator.FindSequenceOfDays(list_of_dates[x],
                                                                   list_of_dates[x + 1]).generate_sequence()
        for ss in return_list:
            serial_dates.append(ss.strftime('%Y-%m-%d'))
    '''
    for x in serial_dates:
        print(x)
    '''
    f = 0
    for x in serial_dates:
        if x == inputed_entry_date or x == inputed_exit_date:
            f = 1
            break
        elif inputed_entry_date < x and inputed_exit_date > x:
            f = 1
            break
    if f == 1:
        cabinBookingList = []
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "SELECT CABIN_ID,TO_CHAR(ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(EXIT_DATE,'yyyy-mm-dd') from CABIN_USER_APPOINTMENT where CABIN_ID = " + str(
            cabin_id)
        c.execute(statement)
        index = 1
        for row in c:
            cabinBookingList.append(cabinBookingDetails(index, row[0], row[1], row[2]))
            index = index + 1
        conn.close()
        return render(request, "cabin/cabin_booking_error_page_by_user.html",
                      {'uch': cabinBookingList, 'cabin_id': request.GET['cabin_id_for_user']})
    else:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
        c = conn.cursor()
        statement = "INSERT INTO MEDI_SHEBA.CABIN_USER_APPOINTMENT(USER_ID,CABIN_ID,ENTRY_DATE,EXIT_DATE,USER_TYPE) " \
                    "VALUES" \
                    " (" + "\'" + str(user_info['pk']) + "\'," + "\'" + str(
            cabin_id) + "\'," + "TO_DATE(" + "\'" + inputed_entry_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," \
                    + "TO_DATE(" + "\'" + inputed_exit_date + "\'," + "\'" + "yyyy-mm-dd" + "\')," + "\'" + \
                    user_info['type'] + "\'" + ")"
        c.execute(statement)
        conn.commit()
        return redirect("submit_book_cabin_by_user")


def submit_book_cabin_by_user(request):
    return render(request, "cabin/cabin_booking_confirmation_by_user.html")


def go_to_user_home(request):
    return redirect("user_home")


def cabin_booking_history_by_user(request):
    cabinBookingList = []
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()
    statement = "SELECT USER_ID,CABIN_ID,TO_CHAR(ENTRY_DATE,'yyyy-mm-dd'),TO_CHAR(EXIT_DATE,'yyyy-mm-dd'),USER_TYPE from CABIN_USER_APPOINTMENT where USER_ID= " + str(
        user_info['pk']) + " AND USER_TYPE = " + "\'" + user_info['type'] + "\'"
    c.execute(statement)
    print(statement)
    index = 1
    for row in c:
        cabinBookingList.append(cabinBookingHistory(index, row[0], row[1], row[2], row[3], row[4]))
        index = index + 1
    conn.close()
    return render(request, "cabin/cabin_booking_history_by_user.html", {'cbh': cabinBookingList})


'''
  cabin ends
'''


# TODO:Doctor user appointment

def doctor_schedule(request):
    start_hour = request.POST['start_hour']
    start_minute = request.POST['start_minute']
    end_hour = request.POST['end_hour']
    end_minute = request.POST['end_minute']
    weekday = request.POST['weekday']
    max_app = request.POST['max_app']

    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
    conn = cx_Oracle.connect(user='MEDI_SHEBA', password='1234', dsn=dsn_tns)
    c = conn.cursor()

    statement = ""

    if weekday == "Saturday":
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET SAT_START = " + str(start_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET SAT_END = " + str(end_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET SAT_MAX = " + str(max_app) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
    elif weekday == "Sunday":
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET SUN_START = " + str(start_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET SUN_END = " + str(end_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET SUN_MAX = " + str(max_app) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
    elif weekday == "Monday":
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET MON_START = " + str(start_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET MON_END = " + str(end_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET MON_MAX = " + str(max_app) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
    elif weekday == "Tuesday":
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET TUES_START = " + str(start_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET TUES_END = " + str(end_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET TUES_MAX = " + str(max_app) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
    elif weekday == "Wednesday":
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET WED_START = " + str(start_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET WED_END = " + str(end_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET WED_MAX = " + str(max_app) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
    elif weekday == "Thursday":
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET THU_START = " + str(start_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET THU_END = " + str(end_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET THU_MAX = " + str(max_app) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
    elif weekday == "Friday":
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET FRI_START = " + str(start_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET FRI_END = " + str(end_hour) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
        statement = "UPDATE MEDI_SHEBA.DOCTOR_SCHEDULE SET FRI_MAX = " + str(max_app) + " WHERE DOCTOR_ID = " \
                    + str(user_info['pk'])
        c.execute(statement)
        conn.commit()
    return render(request, "schedule_editor/add_schedule_confirmation.html")


def redirect_to_schedule_doctor_schedule(request):
    return redirect("doctor_change_schedule")


def redirect_to_home_doctor_schedule(request):
    return redirect("doctor_home")
