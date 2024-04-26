from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User
from .forms import UpdateProfileForm
from company.decorators import allowed_users
from django.contrib import messages


@login_required(login_url='login')
@allowed_users(['EMPLOYEE'])
def updateProfile(request):

	sub_menu = 'update_profile'
	selected_user = request.user
	formset = UpdateProfileForm(instance=selected_user)
	
	if request.method == 'POST':
		try:
			english_name = request.POST['english_name']
			arabic_name = request.POST['arabic_name']
			if english_name == "" or arabic_name == "":
				messages.error(request, f"You should fill out all fields!", 'danger')
				return redirect('myProfile')
			
			if len(english_name) < 3 or len(arabic_name) < 3:
				messages.error(request, f"Your name should contains more than 2 letters!", 'danger')
				return redirect('myProfile')

			selected_user.english_name = english_name.capitalize()
			selected_user.arabic_name = arabic_name
			selected_user.save()

			messages.success(request, f"Profile updated successfully!")
			return redirect('myProfile')
		
		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('myProfile')
	
	context = {'title': selected_user.english_name + " - Update", 'selected_user':selected_user,
				'formset':formset, 'sub_menu':sub_menu}
	
	return render(request, "mail/settings/update_profile.html", context)


@login_required(login_url='login')
@allowed_users(['EMPLOYEE'])
def updatePassword(request):

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
							return redirect('myProfile')
						
					except:
						messages.error(request, f"There is something wrong!", 'danger')
						return redirect('myPassword')
				else:
					messages.error(request, f"New password and confirm password are not match!", 'danger')
					return redirect('myPassword')
			else:
				messages.error(request, f"The current password is not correct!", 'danger')
				return redirect('myPassword')
		except:
			messages.error(request, f"There is something wrong!", 'danger')
			return redirect('myPassword')

	context = {'title': 'Update Password'}

	return render(request, "mail/settings/update_password.html", context)
