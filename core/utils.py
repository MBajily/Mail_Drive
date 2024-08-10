import pyotp
import json
from datetime import datetime, timedelta
from django.core.mail import send_mail
# from twilio.rest import Client
from .models import User
from django.contrib import messages
from TaqnyatSms import client

# with open('config.json') as config_file:
#     config = json.load(config_file)


def sendOTP(request):
    try:
        del request.session['otp_secret_key']
    except:
        pass
    try:
        del request.session['otp_valid_date']
    except:
        pass

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
    try:
        del request.session['otp_secret_key']
    except:
        pass
    try:
        del request.session['otp_valid_date']
    except:
        pass

    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_date'] = str(valid_date)

    username = request.session["username"]
    user = User.objects.get(username=username)

    body = f"Your OTP code is:\n{otp}\nfor Mozal account login."
    sender = "MOZAL"
    bearer = 'e6c8b3890f4c0b81f8604ba78e0f3cfa'
    recipients = [str(user.phone)];
    # sender = 'Taqnyat.sa';

    taqnyt = client(bearer)
    message = taqnyt.sendMsg(body, recipients, sender, str(datetime.now() + timedelta(seconds=5)))

    messages.success(request, f"OTP code sent to your phone number.")
    # print(body)