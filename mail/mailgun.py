import requests
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def send_email(extension, sender, recipient, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{extension}/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": f"Your Name <{sender}>",
              "to": recipient,
              "subject": subject,
              "text": body})


@csrf_exempt
def handle_incoming_email(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body_plain = request.POST.get('body-plain')

        email = Email(
            user=user,
            sender=sender,
            subject=subject,
            body=body,
            read=user == request.user
        )
        email.save()
        for recipient in local_recipients:
            email.local_recipients.add(recipient)
        email.save()
        
        # Process the email (e.g., save to database, notify user)
        
        return HttpResponse('OK')
    return HttpResponse('Method not allowed', status=405)