from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .serializers import EmailSerializer, EmailFilesSerializer
from core.models import User, Company, Employee, Email, Email_File
from django.db.models import Q


@api_view(['GET'])
def getMailbox(request, mailbox):
    if mailbox == "inbox":
        emails = Email.objects.filter(
            user=request.user, recipients=request.user, archived=False, deleted=False,
        )
    elif mailbox == "sent":
        emails = Email.objects.filter(
            user=request.user, sender=request.user, deleted=False,
        )
    elif mailbox == "archive":
        emails = Email.objects.filter(
            user=request.user, archived=True, deleted=False,
        ).filter( Q(sender=request.user) |Q(recipients=request.user))
    elif mailbox == "starred":
        emails = Email.objects.filter(
            user=request.user, starred=True, deleted=False,
        ).filter( Q(sender=request.user) |Q(recipients=request.user))
    elif mailbox == "trash":
        emails = Email.objects.filter(
            user=request.user, deleted=True
        ).filter( Q(sender=request.user) |Q(recipients=request.user))
    
    else:
        return Response({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getEmail(request, pk):
    try:
        email = Email.objects.get(id=pk)
        serializer = EmailSerializer(email, many=False)
        return Response(serializer.data)

    except:
        return Response({"error": "Email does not exist."}, status=404)



@api_view(['GET', 'PUT', 'DELETE'])
def updateEmail(request, pk):

    # Query for requested email
    try:
        email = Email.objects.get(user=request.user, id=pk)
    except Email.DoesNotExist:
        return Response({"error": "Email does not exist."}, status=404)

    if request.method == "GET":
        serializer = EmailSerializer(email, many=False)
        return Response(serializer.data, status=204)

    # Update whether email is read or should be archived
    if request.method == "PUT":
        # data = json.loads(request.body)
        data = request.data
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        if data.get("starred") is not None:
            email.starred = data["starred"]
        if data.get("deleted") is not None:
            email.deleted = data["deleted"]
        email.save()
        serializer = EmailSerializer(email, many=False)
        return Response(serializer.data, status=204)

    elif request.method == "DELETE":
        email.delete()
        return Response({"message": "Email is deleted."}, status=204)
    # email must be via GET or PUT
    else:
        return Response({
            "error": "GET or PUT or DELETE request required."
        }, status=400)



@api_view(['POST'])
def compose(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return Response({"error": "POST request required."}, status=400)

    # Check recipient emails
    # data = json.loads(request.body)
    data = request.data
    emails = [email.strip() for email in data.get("recipients").split(",")]
    if emails == [""]:
        return Response({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(username=email)
            recipients.append(user)
        except User.DoesNotExist:
            return Response({
                "error": f"User with email {email} does not exist."
            }, status=400)

    # Get contents of email
    subject = data.get("subject", "")
    body = data.get("body", "")

    # Create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        email = Email(
            user=user,
            sender=request.user,
            subject=subject,
            body=body,
            read=user == request.user
        )
        email.save()
        for recipient in recipients:
            email.recipients.add(recipient)
        email.save()

    return Response({"message": "Email sent successfully."}, status=201)


@api_view(['POST'])
def searchEmail(request):
    query = request.data.get("query")
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
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response({"error": "No result Found"}, status=404)


