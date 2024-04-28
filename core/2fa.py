from datetime import datetime
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from views import login_redirect_page, get_device


def login_view(request):
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
            return redirect('login')
    else:
        messages.error(request, f"Invalid email and/or password.", 'danger')
        return redirect('login')