from django.shortcuts import render
from core.models import Drive_File
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.
def files(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "drive/files.html")


@login_required
def drivebox(request, drivebox):

    # Filter emails returned based on drivebox
    if drivebox == "home":
        emails = Drive_File.objects.filter(
            user=request.user, archived=False, deleted=False,
        )
    elif drivebox == "recent":
        emails = Drive_File.objects.filter(
            user=request.user, deleted=False,
        ).order_by("-timestamp")
    elif drivebox == "archive":
        emails = Drive_File.objects.filter(
            user=request.user, archived=True, deleted=False,
        )
    elif drivebox == "starred":
        emails = Drive_File.objects.filter(
            user=request.user, starred=True, deleted=False,
        )
    elif drivebox == "trash":
        emails = Drive_File.objects.filter(
            user=request.user, deleted=True
        )
    
    else:
        return JsonResponse({"error": "Invalid drivebox."}, status=400)

    # Return emails in reverse chronologial order
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)