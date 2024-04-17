import secrets
import re
from django.shortcuts import render, redirect
from core.models import User, Employee
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


def generate_password(email):
	password_length = 12  # Change this to your desired password length

	password = secrets.token_urlsafe(password_length)
	hashed_password = make_password(password)

	# final_password = "pbkdf2_sha256$600000$mBOx9Z3WgBosn5Q4ney00S$kj7blpWxdmL/ub3mtO50aN358/CSKAPHOE8WEV2TZGM="

	return {"final_password":hashed_password, "password":password}


#=====================================================
#==================== employees =======================
#=====================================================
#------------------ Show employees --------------------
@login_required(login_url='login')
@allowed_users(['COMPANY'])
def employees(request):
	main_menu = 'employees'
	sub_menu = 'all_employees'
	
	all_employees = User.objects.filter(is_deleted=False).filter(company=request.user.id).filter(role="EMPLOYEE").all()
	
	context = {'title':'Our Employees','all_employees':all_employees,
				'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'company/employees/employees.html', context)
#-----------------------------------------------------

#----------------- Create employee -------------------
@login_required(login_url='login')
@allowed_users(['COMPANY'])
def addEmployee(request):
	main_menu = 'employees'
	sub_menu = 'add_employee'
	
	formset = EmployeeForm()
	
	if request.method == 'POST':
		english_name = request.POST['english_name'].capitalize()
		arabic_name = request.POST['arabic_name']
		email = request.POST['email'].lower()
		username = request.POST['username'].lower().split('@')[0]
		username = str(username) + '@' + str(request.user.extension)
		password = generate_password(email)
		if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", username):
			return redirect('addEmployee')

		formset = Employee(english_name=english_name, arabic_name=arabic_name, password=password["final_password"],
						   email=email, username=username, company=request.user)
		
		message = f"Hi {formset.english_name},\n"
		message += f"Your account is created successfully on Samail Mailing Platform.\n"
		message += f"Your login details is:\n"
		message += f"- Email: {formset.username}\n"
		message += f"- Password: {password['password']}\n\n"

		message += f"You can change the password after login to your account, go to login page: https://emailsaudi.com/login\n\n"

		message += f"Thank you,\n"
		message += f"Samail Team."
		if formset:
			formset.save()
			send_mail(
				"Login Details to Samail Platform",
				message,
				"mozal.samail@gmail.com",
				[f"{formset.email}"],
				fail_silently=False,
			)
		
		return redirect('employees')
	
	context = {'title':'Add employee', 'formset':formset,
				'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'company/employees/employee_create.html', context)
#-----------------------------------------------------


#--------------- Deactivate employee -----------------
@allowed_users(['COMPANY'])
def deactivateEmployee(request, employee_id):
	main_menu = 'employees'
	sub_menu = 'all_employees'
	
	User.objects.filter(id=employee_id).update(is_active=False)
	
	return redirect('employees')
#----------------------------------------------------


#--------------- Activate employee -------------------
@allowed_users(['COMPANY'])
def activateEmployee(request, employee_id):
	main_menu = 'employees'
	sub_menu = 'all_employees'
	
	User.objects.filter(id=employee_id).update(is_active=True)
	
	return redirect('employees')
#----------------------------------------------------


#--------------- Delete employee -------------------
@allowed_users(['COMPANY'])
def deleteEmployee(request, employee_id):
	main_menu = 'employees'
	sub_menu = 'all_employees'
	
	User.objects.filter(id=employee_id).update(is_active=False)
	User.objects.filter(id=employee_id).update(is_deleted=True)
	
	return redirect('employees')
#----------------------------------------------------
#=====================================================
#=====================================================
#=====================================================