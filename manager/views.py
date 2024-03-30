import hashlib
import os
import secrets
import base64
import re
from django.shortcuts import render, redirect
from core.models import Company, User
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from .forms import PartnerForm, UpdatePartnerForm
from django.views.decorators.csrf import csrf_exempt

def generate_password():
	# password_length = 12  # Change this to your desired password length
	# iterations = 600000  # Change this to your desired number of iterations

	# salt = secrets.token_bytes(16)
	# password = secrets.token_urlsafe(password_length)

	# hashed_password = hashlib.pbkdf2_hmac(
	#     'sha256',  # Hashing algorithm
	#     password.encode('utf-8'),  # Password to hash
	#     salt,  # Salt
	#     iterations  # Number of iterations
	# )

	# hashed_password = base64.b64encode(hashed_password).decode('utf-8')
	# salt = base64.b64encode(salt).decode('utf-8')

	# final_password = f"pbkdf2_sha256${iterations}${salt}${hashed_password}"

	final_password = "pbkdf2_sha256$600000$mBOx9Z3WgBosn5Q4ney00S$kj7blpWxdmL/ub3mtO50aN358/CSKAPHOE8WEV2TZGM="

	return final_password

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
		if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", username):
			return redirect('partners')

		formset = Company(english_name=english_name, arabic_name=arabic_name, password=generate_password(),
							extension=extension, photo=photo, email=email, username=username)
		if formset:
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