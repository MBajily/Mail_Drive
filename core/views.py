import re
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import User
from project import settings
from user_agents import parse
from django.core.mail import send_mail
from django.contrib import messages
from .utils import sendOTP, sendSMSOTP
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

    def form_valid(self, form):
        messages.success(self.request, 'Password reset successful.')
        return super().form_valid(form)
    

def get_device(request):
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    
    # Access device information
    device_type = user_agent.device.family
    os = user_agent.os.family
    os_version = user_agent.os.version_string
    
    return f"{device_type} ({os} {os_version})"


@csrf_exempt
def is_username_exists(request):
    username = request

    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False



@api_view(['POST'])
def passwordReset(request):
    try:
        data = request.data
        username = data.get("username")
        if is_username_exists(username) == False:
            # return Response({"error": "This email doesn't exist"}, status=404)
            messages.error(request, f"This email doesn't exist", 'danger')
            return redirect("passwordReset")

        selectedUser = User.objects.get(username=username)
        form = PasswordResetForm({"email": selectedUser.email, "username": selectedUser.username, "site_name":"Mozal"})
        if form.is_valid():
            form.save(
                request=request,
                from_email=settings.DEFAULT_FROM_EMAIL,
                # email_template_name='registration/password_reset_email.html',
                # subject_template_name='registration/password_reset_subject.txt',
            )
            # return Response({"message": "We sent you a reset password url on your email."}, status=202)
            messages.success(request, f"We sent you a reset password url on your email.")
            return redirect("login")
        else:
            messages.error(request, f"There is something wrong!", 'danger')
            return redirect("passwordReset")

    except Exception:
        messages.error(request, f"There is something wrong!", 'danger')
        return redirect("passwordReset")



@login_required(login_url='login')
def login_redirect_page(request):
    user = request.user
    if user.is_superuser == True:
        return redirect("partners")

    if user.role == 'COMPANY':
        print("Done")
        return redirect("employees")

    elif user.role == 'EMPLOYEE':
        return redirect("index")

    else:
        return redirect('login')


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "mail/inbox.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.user.is_authenticated:
        return redirect(login_redirect_page)
        
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["email"].lower()
        password = request.POST["password"]

        if username == "" or password == "":
            messages.error(request, f"You should fill out all fields!", 'danger')
            return redirect('login')
        
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", username):
            messages.error(request, f"Email field: an invalid email!", 'danger')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            request.session['username'] = username
            # sendOTP(request)
            # sendSMSOTP(request)
            return redirect('emailOTP')
        
        else:
            messages.error(request, f"Invalid email and/or password.", 'danger')
            return redirect('login')
    else:
        return render(request, "mail/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def files(request):
    if request.user.is_authenticated:
        return render(request, "drive/files.html")

    return redirect('login')


def resetPasswordRequest(request):
    return render(request, "reset_password/password_reset_request.html")


def sign_up(request):
    return render(request, "authentications/sign_up.html")


def home(request):
    return render(request, "home/en/home.html")


def getStartedPage(request):
    return render(request, "home/en/get_started.html")


def privacy_policy(request):
    return render(request, 'home/en/privacy_policy.html')


def terms_and_conditions(request):
    return render(request, 'home/en/terms_and_conditions.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('con_name')
        email = request.POST.get('con_email')
        subject = request.POST.get('subject')
        message = request.POST.get('con_message')
        
        # Compose email
        email_subject = f"New contact form submission: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        # Send email
        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        
        # Redirect after successful submission
        return HttpResponse(status=200, content="Message sent successfully.")
    
    return HttpResponse(status=400, content="Invalid request.")


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            return redirect('home')
        
        # Check if email is not empty
        if not email:
            messages.error(request, "Email address cannot be empty.")
            return redirect('home')
        
        # Check email length
        if len(email) > 254:  # Maximum length for an email address
            messages.error(request, "Email address is too long.")
            return redirect('home')
        
        # Compose email
        email_subject = f"New subscriber"
        email_message = f"Email: {email}"

        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except:
            return redirect('home')
        
        # Redirect after successful submission
        return redirect('home')
    
    return redirect('home')
