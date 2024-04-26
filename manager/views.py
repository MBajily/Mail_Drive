import secrets
import re
from django.shortcuts import render, redirect
from core.models import Company, User
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from .forms import PartnerForm, UpdatePartnerForm
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
#==================== partners =======================
#=====================================================
#------------------ Show partners --------------------
@login_required(login_url='login')
@admin_only
def partners(request):
	main_menu = 'partners'
	sub_menu = 'all_partners'
	
	all_partners = User.objects.filter(role="COMPANY").all()
	
	context = {'title':'Our partners','all_partners':all_partners,
				'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'manager/partners/partners.html', context)
#-----------------------------------------------------

#----------------- Create partner -------------------
@login_required(login_url='login')
@admin_only
def addPartner(request):
	main_menu = 'partners'
	sub_menu = 'add_partner'
	
	formset = PartnerForm()
	
	if request.method == 'POST':
		try:
			english_name = request.POST['english_name'].capitalize()
			arabic_name = request.POST['arabic_name']
			email = request.POST['email'].lower()
			extension = request.POST['extension'].lower().split('@')[-1]
			photo = request.FILES['photo']
			username = 'admin' + '@' + str(extension)

			if is_email_exists(email) and is_username_exists(username):
				messages.error(request, f"Email '{email}' is already used!", 'danger')
				messages.error(request, f"Extension '{extension}' is already used!", 'danger')
				return redirect('addPartner')

			elif is_email_exists(email):
				messages.error(request, f"Email '{email}' is already used!", 'danger')
				return redirect('addPartner')
			
			elif is_username_exists(username):
				messages.error(request, f"Extension '{extension}' is already used!", 'danger')
				return redirect('addPartner')
			
			password = generate_password(email)
			if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", username):
				messages.error(request, f"Email '{username}' is invalid email!", 'danger')
				return redirect('addPartners')

			formset = Company(english_name=english_name, arabic_name=arabic_name, password=password["final_password"],
								extension=extension, photo=photo, email=email, username=username)
			
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

				messages.success(request, f"'{english_name}' company has added successfully!")
			return redirect('partners')
		
		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('addPartner')
	
	context = {'title':'Add partner', 'formset':formset,
				'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'manager/partners/partner_create.html', context)
#-----------------------------------------------------

#----------------- Update partner --------------------
@login_required(login_url='login')
@admin_only
def updatePartner(request, partner_id):
	main_menu = 'partners'
	sub_menu = 'all_partners'
	
	selected_partner = User.objects.get(id=partner_id)
	formset = UpdatePartnerForm(instance=selected_partner)
	
	if request.method == 'POST':
		try:
			if 'photo' in request.FILES:
				# Delete the old photo if it exists
				if selected_partner.photo:
					default_storage.delete(selected_partner.photo.name)
				selected_partner.photo = request.FILES['photo']
		
		except:
			messages.error(request, f"There is something wrong. Please choose other photo!", 'danger')
			return redirect('updatePartner')
		
		try:
			selected_partner.english_name = request.POST['english_name'].capitalize()
			selected_partner.arabic_name = request.POST['arabic_name']
			selected_partner.save()

			messages.success(request, f"Updated successfully!")
			return redirect('updatePartner')
		
		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('updatePartner')
	
	context = {'title': selected_partner.english_name + " - Update", 'selected_partner':selected_partner,
				'formset':formset, 'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'manager/partners/partner_update.html', context)
#----------------------------------------------------


#--------------- Deactivate partner -----------------
@admin_only
def deactivatePartner(request, partner_id):
	User.objects.filter(id=partner_id).update(is_active=False)
	User.objects.filter(company=partner_id).update(is_active=False)
	
	return redirect('partners')
#----------------------------------------------------


#--------------- Activate partner -------------------
@admin_only
def activatePartner(request, partner_id):
	User.objects.filter(id=partner_id).update(is_active=True)
	User.objects.filter(company=partner_id).update(is_active=True)

	return redirect('partners')
#----------------------------------------------------
#=====================================================
#=====================================================
#=====================================================



@login_required(login_url='login')
@admin_only
def adminPassword(request):
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
							return redirect('partners')
						
					except:
						messages.error(request, f"There is something wrong!", 'danger')
						return redirect('adminPassword')
				else:
					messages.error(request, f"New password and confirm password are not match!", 'danger')
					return redirect('adminPassword')
			else:
				messages.error(request, f"The current password is not correct!", 'danger')
				return redirect('adminPassword')
		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('adminPassword')

	context = {'title': 'Update Password', 
				'main_menu':main_menu, 'sub_menu':sub_menu}

	return render(request, 'manager/update_password.html', context)