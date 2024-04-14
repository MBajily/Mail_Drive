import secrets
import re
from django.shortcuts import render, redirect
from core.models import Company, User
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from .forms import PartnerForm, UpdatePartnerForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


def generate_password(email):
	password_length = 12  # Change this to your desired password length

	password = secrets.token_urlsafe(password_length)
	hashed_password = make_password(password)

	# final_password = "pbkdf2_sha256$600000$mBOx9Z3WgBosn5Q4ney00S$kj7blpWxdmL/ub3mtO50aN358/CSKAPHOE8WEV2TZGM="

	return {"final_password":hashed_password, "password":password}


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
		english_name = request.POST['english_name'].capitalize()
		arabic_name = request.POST['arabic_name']
		email = request.POST['email'].lower()
		extension = request.POST['extension'].lower().split('@')[-1]
		photo = request.FILES['photo']
		username = 'admin' + '@' + str(extension)
		password = generate_password(email)
		if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", username):
			return redirect('partners')

		formset = Company(english_name=english_name, arabic_name=arabic_name, password=password["final_password"],
							extension=extension, photo=photo, email=email, username=username)
		
		message = f"""
		Hi {formset.english_name},
		Your account is created successfully on Samail Mailing Platform.
		Your login details is:
		- Email: {formset.username}
		- Password: {password["password"]}

		You can change the password after login to your account, go to login page: http://127.0.0.1:8000/api/v1/login

		Thank you,
		Samail Team.
		"""

		if formset:
			send_mail(
				"Login Details to Samail Platform",
				message,
				"mozal.samail@gmail.com",
				[f"{formset.email}"],
				fail_silently=False,
			)
			formset.save()
		
		return redirect('partners')
	
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
		english_name = request.POST['english_name'].capitalize()
		arabic_name = request.POST['arabic_name']
		photo = request.FILES['photo']
		if selected_partner.photo:
			selected_partner.photo.delete()
		
		User.objects.filter(id=partner_id).update(english_name=english_name)
		User.objects.filter(id=partner_id).update(arabic_name=arabic_name)
		selected_partner.photo=photo
		selected_partner.save()

		return redirect('partners')
	
	context = {'title': selected_partner.english_name + " - Update", 'selected_partner':selected_partner,
				'formset':formset, 'main_menu':main_menu, 'sub_menu':sub_menu}
	
	return render(request, 'manager/partners/partner_update.html', context)
#----------------------------------------------------


#--------------- Deactivate partner -----------------
@admin_only
def deactivatePartner(request, partner_id):
	main_menu = 'partners'
	sub_menu = 'all_partners'
	
	User.objects.filter(id=partner_id).update(is_active=False)
	User.objects.filter(company=partner_id).update(is_active=False)
	
	return redirect('partners')
#----------------------------------------------------


#--------------- Activate partner -------------------
@admin_only
def activatePartner(request, partner_id):
	main_menu = 'partners'
	sub_menu = 'all_partners'
	
	User.objects.filter(id=partner_id).update(is_active=True)
	User.objects.filter(company=partner_id).update(is_active=True)

	return redirect('partners')
#----------------------------------------------------
#=====================================================
#=====================================================
#=====================================================