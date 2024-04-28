import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import User

def sendOTP(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_date)

    username = request.session["username"]
    user = User.objects.get(username=username)
    message = f"Hi {user.english_name},\n\nUse the one time password below to authorize your account {otp}.\n\n"
    message += f"Thanks & Best Regards."

    send_mail(
        "Two-Factor Authentication emailsaudi.com",
        message,
        "mozal.samail@gmail.com",
        [f"{user.email}"],
        fail_silently=False,
    )

    # print(f"OTP = {otp}")