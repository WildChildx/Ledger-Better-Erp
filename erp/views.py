from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import mysql.connector
from mysql.connector import errorcode
# import requests  # to connect with yash backend


# localdb
# mydb = mysql.connector.connect(
# host="localhost",
# user="dbms",
#  password="Dbms@1234",
# database = 'erp'
# )

# remote db on docker yash
mydb = mysql.connector.connect(
    host="dbms-mini-project.duckdns.org",
    user="dbms",
    password="dbms",
    database='erp'
)

loged_in_user_roll = ''
loged_in_user_name = ''
passwords = ['gaurav']


def home(request):
    return render(request, 'loginOptions.html')


def studentLogin(request):
    print('studentLogin')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        mycursor = mydb.cursor()
        mycursor.execute(
            "select password,name,is_admitted from students where roll_no = %s", (roll_no,))
        try:
            user = mycursor.fetchall()[0]
            mycursor.close()
            if(password == user[0] and user[2] == 1):
                global loged_in_user_roll, loged_in_user_name
                loged_in_user_roll = roll_no
                loged_in_user_name = user[1]
                return redirect('/studentDash')
            elif(user[2] == 0):
                return render(request, 'studentLogin.html', {'invalid_password': 'Acception pending'})
            return render(request, 'studentLogin.html', {'invalid_password': 'Invalid password'})
        except IndexError:
            return render(request, 'studentLogin.html', {'invalid_username': 'Invalid Username'})
    return render(request, 'studentLogin.html')


def studentDash(request):
    # r = requests.get(
    #     f"http://dbms-mini-project.duckdns.org:3000/student/status/{loged_in_user_roll}")
    # print(loged_in_user_roll)
    # print(r.json()[0]['percentage'])
    context = {
        'roll': loged_in_user_roll,
        'name': loged_in_user_name,
    }
    return render(request, 'studentDash.html', context)


def createStudent(request):
    print("in register")
    if request.method == 'POST':
        print("in register POST")
        name = request.POST.get('name')
        roll_no = request.POST.get('roll')
        year = request.POST.get('year')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(name, '', roll_no, '', year, '', mail,
              '', contact, '', password1, '', password2)
        mycursor = mydb.cursor()
        sql = "select roll_no from students"
        mycursor.execute(sql)
        roll = mycursor.fetchall()[0]
        print(roll)
        mycursor.close()
        error = 0
        context = {
            'error1': '',
            'error2': '',
            'error3': '',
            'error4': '',
            'error5': '',
        }
        if(roll_no in roll):
            print(roll[0], '', roll_no)
            context['error1'] = 'user allready Registerd'
            error = 1
            # return render(request, 'register.html',{'error1' : 'user allready Registerd'})
        if((roll_no[: 1].isdigit() == False) or (roll_no[2: 3].isalpha() == False) or (roll_no[4:].isdigit() == False)):
            print(roll_no)
            error = 1
            context['error1'] = 'Invalid Username'

        if ((contact.isdigit() == False) or (len(str(contact)) != 10)):
            context['error2'] = 'Enter Valid phone number'
            error = 1
            # return render(request, 'register.html', {'error2' : 'Enter Valid phone number'})

        if (password1 != password2):
            context['error3'] = 'passwords do not matched'
            error = 1
            # return render(request, 'register.html', {'error3' : 'passwords do not matched'})
        if(error == 1):
            return render(request, 'createStudent.html', context)
        mycursor = mydb.cursor()
        sql = 'insert into students(Roll_no,name,contact_no,mail_id,year,password,is_admitted) values(%s,%s,%s,%s,%s,%s,%s)'
        val = (roll_no, name, contact, mail, year, password1, 0)
        mycursor.execute(sql, val)
        mydb.commit()
        # r = requests.post("http://dbms-mini-project.duckdns.org:3000/student", json={
        #                   'student': {'name': name, 'roll': roll_no, 'class': 1, 'password': password1}})
        # print(r)
        return redirect('/studentLogin')
    return render(request, 'createStudent.html')


def teacher(request):
    print('here')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        mycursor = mydb.cursor()
        sql = "select name,password from teacher where name = %s"
        mycursor.execute(sql, (username,))

        try:
            user = mycursor.fetchall()[0]
            print(user)
            mycursor.close()
            if(password == user[1]):
                global loged_in_user_roll, loged_in_user_name
                loged_in_user_roll = id
                loged_in_user_name = user[0]
                print(user[1], '', password)
                return redirect('/teacher-dashboard')
            return render(request, 'teacher.html', {'invalid_password': 'Invalid password'})
        except IndexError:
            return render(request, 'teacher.html', {'invalid_username': 'Invalid Username'})

        # print('There')
        # return render(request, 'login.html',{'error' : 'Invalid Credentials'})
    return render(request, 'teacher.html')


def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')


def admin(request):
    print('here')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        mycursor = mydb.cursor()
        sql = "select username,password from admin where username = %s"
        mycursor.execute(sql, (username,))

        try:
            user = mycursor.fetchall()[0]
            print(user)
            mycursor.close()
            if(password == user[1]):
                global loged_in_user_roll, loged_in_user_name
                loged_in_user_roll = id
                loged_in_user_name = user[0]
                print(user[1], '', password)
                return redirect('/admin-dashboard')
            return render(request, 'admin.html', {'invalid_password': 'Invalid password'})
        except IndexError:
            return render(request, 'admin.html', {'invalid_username': 'Invalid Username'})

    return render(request, 'admin.html')


def admin_dashboard(request):
    mycursor = mydb.cursor()
    sql = "select roll_no AS roll,name AS name from students where is_admitted = %s"
    status = '0'
    mycursor.execute(sql, (status,))
    print(mycursor)
    students = [{'roll': x[0], 'name':x[1]} for x in mycursor.fetchall()]
    print(students)
    # mycursor.close()
    return render(request, 'admin_dashboard.html', {'students': students})


def acceptUser(request):
    if request.method == 'POST':
        roll_no = request.POST.get('roll')
        method = request.POST.get('action')
        mycursor = mydb.cursor()
        query = "update students set is_admitted = 1 where roll_no = %s"
        mycursor.execute(query, (roll_no,))
        mydb.commit()
        return HttpResponse("Student Accepted")
    return HttpResponse("User Updation Failed")


def rejectUser(request):
    if request.method == 'POST':
        roll_no = request.POST.get('roll')
        method = request.POST.get('action')
        mycursor = mydb.cursor()
        query = "delete from students where roll_no = %s"
        mycursor.execute(query, (roll_no,))
        mydb.commit()
        return HttpResponse("Student Rejected")
    return HttpResponse("User Rejection Failed")
