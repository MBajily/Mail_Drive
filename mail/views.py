import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from functools import reduce
import operator
from core.models import User, Email
from django.core.mail import EmailMessage


@login_required(login_url='login')
def login_redirect_page(request):
    user = request.user
    if user.is_superuser == True:
        return redirect("partners")

    if user.role == 'COMPANY':
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


@csrf_exempt
@login_required
def compose(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    try:
        # Check recipient emails
        data = json.loads(request.body)
        emails = [email.strip() for email in data.get("recipients").split(",")]
        if emails == [""]:
            return JsonResponse({
                "error": "At least one recipient required."
            }, status=400)

        # Convert email addresses to users
        local_recipients = []
        global_recipients = []
        for email in emails:
            try:
                user = User.objects.get(username=email.lower())
                local_recipients.append(user)
            except User.DoesNotExist:
                # return JsonResponse({
                #     "error": f"User with email {email} does not exist."
                # }, status=400)
                global_recipients.append(email)

        # Get contents of email
        subject = data.get("subject", "")
        body = data.get("body", "")

        # Create one email for each recipient, plus sender
        users = set()
        users.add(request.user)
        users.update(local_recipients)
        for user in users:
            email = Email(
                user=user,
                sender=request.user,
                subject=subject,
                body=body,
                read=user == request.user
            )
            email.save()
            for recipient in local_recipients:
                email.local_recipients.add(recipient)
            email.save()
        
        message = f"<b>You received this message from {request.user.email} from EmailSaudi.com platform. The content of the message is as follows:</b>"
        message += "<br><br>"
        message += "#"
        message += body
        message += "#"
        message += "<br><br>"
        message += "<i>**Do not replay to this message.</i>"
        send_email = EmailMessage(
        subject=subject,
        body=message,
        from_email="mozal.samail@gmail.com",
        to=global_recipients,
        )
        send_email.content_subtype = "html"  # Set the content type as HTML
        send_email.send(fail_silently=False)

        return JsonResponse({"message": "Email sent successfully."}, status=201)
    
    except:
        return JsonResponse({"error": "There is some thing wrong!"}, status=400)


@login_required
def mailbox(request, mailbox):
    print(request.user.username)

    # Filter emails returned based on mailbox
    if mailbox == "inbox":
        emails = Email.objects.filter(
            user=request.user.username, recipients=request.user, archived=False, deleted=False,
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            user=request.user.username, sender=request.user.username, deleted=False, archived=False,
        )
    elif mailbox == "archive":
        emails = Email.objects.filter(
            user=request.user.username, archived=True, deleted=False,
        ).filter( Q(sender=request.user.username) |Q(recipients=request.user))
    elif mailbox == "starred":
        emails = Email.objects.filter(
            user=request.user.username, starred=True, deleted=False,
        ).filter( Q(sender=request.user.username) |Q(recipients=request.user))
    elif mailbox == "trash":
        emails = Email.objects.filter(
            user=request.user.username, deleted=True
        ).filter( Q(sender=request.user.username) |Q(recipients=request.user))
    
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)


@csrf_exempt
@login_required
def email(request, email_id):

    # Query for requested email
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        if data.get("starred") is not None:
            email.starred = data["starred"]
        if data.get("deleted") is not None:
            email.deleted = data["deleted"]
        email.save()
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        email.delete()
        return HttpResponse(status=204)
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT or DELETE request required."
        }, status=400)

@csrf_exempt
@login_required
def search(request, query):
    if " " in query:
        queries = query.split(" ")
        qset1 =  reduce(operator.__or__, [Q(sender__email__icontains=query)
            | Q(sender__english_name__icontains=query)
            | Q(sender__arabic_name__icontains=query)
            | Q(subject__icontains=query)
            | Q(body__icontains=query) for query in queries])
        results = Email.objects.filter(user=request.user).filter(qset1).distinct()
    else:
        results = Email.objects.filter(user=request.user)\
            .filter(Q(sender__email__icontains=query) 
            | Q(sender__english_name__icontains=query)
            | Q(sender__arabic_name__icontains=query) 
            | Q(subject__icontains=query) 
            | Q(body__icontains=query)).distinct()
    if results:
        emails = results.order_by("-timestamp").all().distinct()
        return JsonResponse([email.serialize() for email in emails], safe=False)
    else:
        return JsonResponse({"error": "No result Found"}, status=404)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(login_redirect_page)
        else:
            return render(request, "mail/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "mail/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# def register(request):
#     if request.method == "POST":
#         email = request.POST["email"]
#         name = request.POST["fname"]
#         arabic_name = request.POST["lname"]
#         # Ensure password matches confirmation
#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
        
#         if password != confirmation:
#             return render(request, "mail/register.html", {
#                 "message": "Passwords must match."
#             })

#         # Attempt to create new user
#         try:
#             user = User.objects.create_user(username=email,email=email,password=password,name=name,arabic_name=arabic_name)
#             user.save()
#         except IntegrityError as e:
#             return render(request, "mail/register.html", {
#                 "message": "Email address already taken."
#             })
#         login(request, user)
#         return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "mail/register.html")
