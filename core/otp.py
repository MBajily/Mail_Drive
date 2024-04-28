import pyotp
from datetime import datetime
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .models import User
from .views import get_device


def emailOTP(request):
    if request.method == "POST":
        otp = request.POST['otp_code']
        username = request.session["username"]
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']
        # Check if authentication successful
        if username and otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.fromisoformat(otp_valid_date)
            if valid_date > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=120)
                if totp.verify(otp):
                    try:
                        user = User.objects.get(username=username)
                        login(request, user)
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
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

                        return redirect("login_redirect_page")
                    
                    except:
                        messages.error(request, f"Invalid email and/or password.", 'danger')
                        return redirect('login')
                else:
                    messages.error(request, f"Invalid OTP Code.", 'danger')
                    return redirect('emailOTP')
            else:
                messages.error(request, f"Invalid OTP Code.", 'danger')
                return redirect('emailOTP')
        else:
            messages.error(request, f"Invalid OTP Code.", 'danger')
            return redirect('login')
    return render(request, 'authentications/email_otp.html')