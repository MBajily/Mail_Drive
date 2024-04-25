from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .forms import UpdateProfileForm
from company.decorators import allowed_users


@login_required(login_url='login')
@allowed_users(['EMPLOYEE'])
def updateProfile(request):

	sub_menu = 'update_profile'
	selected_user = request.user
	formset = UpdateProfileForm(instance=selected_user)
	
	if request.method == 'POST':
		selected_user.english_name = request.POST['english_name'].capitalize()
		selected_user.arabic_name = request.POST['arabic_name']
		selected_user.save()

		return redirect('myProfile')
	
	context = {'title': selected_user.english_name + " - Update", 'selected_user':selected_user,
				'formset':formset, 'sub_menu':sub_menu}
	
	return render(request, "mail/settings/update_profile.html", context)


@login_required(login_url='login')
@allowed_users(['EMPLOYEE'])
def updatePassword(request):

	# Authenticated users view their inbox
	user_logged_in = request.user

	if request.method == 'POST':
		if request.user.check_password(request.POST["current_password"]):
			if request.POST['new_password'] == request.POST['confirm_password']:
				admin_information = User.objects.get(username=user_logged_in.username)
				admin_information.set_password(request.POST['new_password'])
				print(admin_information.password)
				if admin_information:
					admin_information.save()
					return redirect('myProfile')
		else:
			return redirect('myPassword')
	
	return render(request, "mail/settings/update_password.html")
