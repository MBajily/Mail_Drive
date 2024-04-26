import secrets
import re
from django.shortcuts import render, redirect
from core.models import User, Employee
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm
from manager.forms import UpdatePartnerForm
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.contrib import messages


def generate_password(email):
	password_length = 12  # Change this to your desired password length
	password = secrets.token_urlsafe(password_length)
	hashed_password = make_password(password)

	return {"final_password":hashed_password, "password":password}


def is_email_exists(email):
	try:
		User.objects.get(email=email)
		return True
	except User.DoesNotExist:
		return False


def is_username_exists(username):
	try:
		User.objects.get(username=username)
		return True
	except User.DoesNotExist:
		return False
	

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
		try:
			english_name = request.POST['english_name'].capitalize()
			arabic_name = request.POST['arabic_name']
			email = request.POST['email'].lower()
			username = request.POST['username'].lower().split('@')[0]
			username = str(username) + '@' + str(request.user.extension)
			password = generate_password(email)

			if is_email_exists(email) and is_username_exists(username):
				messages.error(request, f"Email '{email}' is already used!", 'danger')
				messages.error(request, f"Username '{username}' is already used!", 'danger')
				return redirect('addEmployee')

			elif is_email_exists(email):
				messages.error(request, f"Email '{email}' is already used!", 'danger')
				return redirect('addEmployee')
			
			elif is_username_exists(username):
				messages.error(request, f"Username '{username}' is already used!", 'danger')
				return redirect('addEmployee')
			
			if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", username) and\
				not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
				messages.error(request, f"'{email}' is invalid email!", 'danger')
				messages.error(request, f"'{username}' is invalid username!", 'danger')
				return redirect('addEmployee')

			elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", username):
				messages.error(request, f"'{username}' is invalid username!", 'danger')
				return redirect('addEmployee')
			
			elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
				messages.error(request, f"'{email}' is invalid email!", 'danger')
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
					"Login Details to emailsaudi.com",
					message,
					"mozal.samail@gmail.com",
					[f"{formset.email}"],
					fail_silently=False,
				)
				messages.success(request, f"Employee '{formset.username}' has added successfully!")

			return redirect('employees')

		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('addEmployee')
	
	context = {'title':'Add employee', 'formset':formset,
				'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'company/employees/employee_create.html', context)
#-----------------------------------------------------


#--------------- Deactivate employee -----------------
@allowed_users(['COMPANY'])
def deactivateEmployee(request, employee_id):
	User.objects.filter(id=employee_id).update(is_active=False)
	
	return redirect('employees')
#----------------------------------------------------


#--------------- Activate employee -------------------
@allowed_users(['COMPANY'])
def activateEmployee(request, employee_id):
	User.objects.filter(id=employee_id).update(is_active=True)
	
	return redirect('employees')
#----------------------------------------------------


#--------------- Delete employee -------------------
@allowed_users(['COMPANY'])
def deleteEmployee(request, employee_id):
	User.objects.filter(id=employee_id).update(is_active=False)
	User.objects.filter(id=employee_id).update(is_deleted=True)
	
	return redirect('employees')
#----------------------------------------------------
#=====================================================
#=====================================================
#=====================================================


@login_required(login_url='login')
@allowed_users(['COMPANY'])
def updatePassword(request):
	main_menu = 'settings'
	sub_menu = 'update_password'

	user_logged_in = request.user

	if request.method == 'POST':
		try:
			if request.user.check_password(request.POST["current_password"]):
				if request.POST['new_password'] == request.POST['confirm_password']:
					try:
						admin_information = User.objects.get(username=user_logged_in.username)
						admin_information.set_password(request.POST['new_password'])
						if admin_information:
							admin_information.save()
							messages.success(request, f"Password updated successfully!")
							return redirect('employees')
					
					except:
						messages.error(request, f"There is something wrong!", 'danger')
						return redirect('updatePassword')
				else:
					messages.error(request, f"New password and confirm password are not match!", 'danger')
					return redirect('updatePassword')
				
			else:
				messages.error(request, f"The current password is not correct!", 'danger')
				return redirect('updatePassword')
			
		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('updatePassword')


	context = {'title': 'Update Password', 
				'main_menu':main_menu, 'sub_menu':sub_menu}

	return render(request, 'company/profile/update_password.html', context)


@login_required(login_url='login')
@allowed_users(['COMPANY'])
def updateProfile(request):
	main_menu = 'settings'
	sub_menu = 'update_profile'
	
	selected_user = request.user
	formset = UpdatePartnerForm(instance=selected_user)
	
	if request.method == 'POST':
		try:
			if 'photo' in request.FILES:
				# Delete the old photo if it exists
				if selected_user.photo:
					default_storage.delete(selected_user.photo.name)
				selected_user.photo = request.FILES['photo']
		
		except:
			messages.error(request, f"There is something wrong. Please choose other photo!", 'danger')
			return redirect('updateProfile')
		
		try:
			english_name = request.POST['english_name']
			arabic_name = request.POST['arabic_name']
			if english_name == "" or arabic_name == "":
				messages.error(request, f"You should fill out all fields!", 'danger')
				return redirect('updateProfile')
			
			if len(english_name) < 3 or len(arabic_name) < 3:
				messages.error(request, f"Your name should contains more than 2 letters!", 'danger')
				return redirect('updateProfile')
			
			selected_user.arabic_name = arabic_name
			selected_user.english_name = english_name.capitalize()
			selected_user.save()		

			messages.success(request, f"Profile updated successfully!")
			return redirect('updateProfile')
		
		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('updateProfile')
	
	context = {'title': selected_user.english_name + " - Update", 'selected_user':selected_user,
				'formset':formset, 'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'company/profile/update_profile.html', context)