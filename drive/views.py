from django.shortcuts import render
from core.models import Drive_File
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from functools import reduce


# Create your views here.
def files(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "drive/files.html")


@login_required
def drivebox(request, drivebox):
    print(drivebox)

    # Filter files returned based on drivebox
    if drivebox == "home":
        files = Drive_File.objects.filter(
            user=request.user, archived=False, deleted=False,
        )
    elif drivebox == "recent":
        files = Drive_File.objects.filter(
            user=request.user, deleted=False,
        )
    elif drivebox == "archive":
        files = Drive_File.objects.filter(
            user=request.user, archived=True, deleted=False,
        )
    elif drivebox == "starred":
        files = Drive_File.objects.filter(
            user=request.user, starred=True, deleted=False,
        )
    elif drivebox == "trash":
        files = Drive_File.objects.filter(
            user=request.user, deleted=True
        )
    
    else:
        return JsonResponse({"error": "Invalid drivebox."}, status=400)

    # Return files in reverse chronologial order
    files = files.order_by("-timestamp").all()
    return JsonResponse([file.serialize() for file in files], safe=False)


@csrf_exempt
@login_required
def search(request, query):
    if " " in query:
        queries = query.split(" ")
        qset1 =  reduce(operator.__or__, [Q(file__icontains=query) for query in queries])
        results = Drive_File.objects.filter(user=request.user).filter(qset1).distinct()
    else:
        results = Drive_File.objects.filter(user=request.user)\
            .filter(Q(file__icontains=query)).distinct()
    if results:
        files = results.order_by("-timestamp").all().distinct()
        return JsonResponse([file.serialize() for file in files], safe=False)
    else:
        return JsonResponse({"error": "No result Found"}, status=404)


@csrf_exempt
@login_required
def markFile(request, file_id):

    # Query for requested email
    try:
        file = Drive_File.objects.get(user=request.user, id=file_id)
    except file.DoesNotExist:
        return JsonResponse({"error": "file not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(file.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        print("here")
        data = json.loads(request.body)
        # if data.get("read") is not None:
        #     file.read = data["read"]
        if data.get("archived") is not None:
            file.archived = data["archived"]
        if data.get("starred") is not None:
            file.starred = data["starred"]
        if data.get("deleted") is not None:
            file.deleted = data["deleted"]
        file.save()
        return HttpResponse(status=204)

    elif request.method == "DELETE":
        file.delete()
        return HttpResponse(status=204)
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT or DELETE request required."
        }, status=400)
