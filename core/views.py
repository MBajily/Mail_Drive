from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from project import settings
from user_agents import parse
from django.core.mail import send_mail
from django.contrib import messages



def get_device(request):
    user_agent = parse(request.META['HTTP_USER_AGENT'])
    
    # Access device information
    device_type = user_agent.device.family
    os = user_agent.os.family
    os_version = user_agent.os.version_string
    
    return f"{device_type} ({os} {os_version})"


# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import MyTokenObtainPairSerializer


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

@csrf_exempt
def is_username_exists(request):
    # data = json.loads(request.body.decode('utf-8'))
    # username = data.get('username')
    username = request

    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False



@api_view(['POST'])
def passwordReset(request):
    try:
        # data = json.loads(request.body.decode('utf-8'))
        data = request.data
        username = data.get("username")
        if is_username_exists(username) == False:
            return Response({"error": "This email doesn't exist"}, status=404)

        selectedUser = User.objects.get(username=username)
        form = PasswordResetForm({"email": selectedUser.email, "username": selectedUser.username, "site_name":"Mozal"})
        if form.is_valid():
            form.save(
                request=request,
                from_email=settings.DEFAULT_FROM_EMAIL,
                # email_template_name='registration/password_reset_email.html',
                # subject_template_name='registration/password_reset_subject.txt',
            )
            return Response({"message": "We sent you a reset password url on your email."}, status=202)
            # return JsonResponse({'success': True, 'message': 'Password reset email has been sent.'})
        else:
            return Response(status=400)
            # return JsonResponse({'success': False, 'errors': form.errors})

    except Exception as e:
        error_data = {
            'error': str(e),
        }
        return Response(error_data, status=400)



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
        email = request.POST["email"].lower()
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            try:
                login(request, user)
                message = f"Hi {request.user.english_name},\n\nWe noticed a new login to your account {request.user.username}.\n\n"
                message += f"Date: {datetime.utcnow().strftime('%d-%b-%Y %H:%M:%S UTC')}\n\nDevice: {get_device(request)}\n\n"
                message += f"If you do not recognize this sign-in, we recommend that you change your password to secure your account."

                send_mail(
                    "Login Alert from emailsaudi.com",
                    message,
                    "mozal.samail@gmail.com",
                    [f"{request.user.email}"],
                    fail_silently=False,
                )

                return redirect(login_redirect_page)
            
            except:
                messages.error(request, f"Invalid email and/or password.", 'danger')
                return render(request, "mail/login.html")
        else:
            messages.error(request, f"Invalid email and/or password.", 'danger')
            return render(request, "mail/login.html")
    else:
        return render(request, "mail/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def files(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "drive/files.html")

    return redirect('login')