import pyotp
import json
from datetime import datetime, timedelta
from django.core.mail import send_mail
from twilio.rest import Client
from .models import User
from django.contrib import messages


# with open('config.json') as config_file:
#     config = json.load(config_file)


def sendOTP(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_date'] = str(valid_date)

    username = request.session["username"]
    user = User.objects.get(username=username)
    message = f"Hi {user.english_name},\n\nUse the one time password below to authorize your account\n{otp}\n\n"
    message += f"Thanks & Best Regards."

    send_mail(
        "Two-Factor Authentication",
        message,
        "mozal.samail@gmail.com",
        [f"{user.email}"],
        fail_silently=False,
    )
    messages.success(request, f"OTP code sent to your email.")

    # print(f"OTP = {otp}")


def sendSMSOTP(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_date)

    # username = request.session["username"]
    # user = User.objects.get(username=username)

    # account_sid = config["TWILIO_SID"]
    # auth_token = config["TWILIO_AUTH_TOKEN"]
    # client = Client(account_sid, auth_token)

    # message = f"Your OTP code is:\n{otp}"
    # sender = "+966538901501"
    # receiver = "+966538900139"
    # verification = client.verify \
    # .v2 \
    # .services('VA00328a018efd4d7867c782176c8c6ca0') \
    # .verifications \
    # .create(to='+966538901501', channel='sms')
    # messages.success(request, f"OTP code sent to phone number.")

    # print(verification.sid)