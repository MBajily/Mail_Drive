from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CompanySerializer, EmployeeSerializer, EmailSerializer, EmailFilesSerializer, DriveSerializer
from .models import Company, Employee, Email, Email_File, Drive_File


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
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)
