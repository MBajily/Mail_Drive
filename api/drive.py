from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DriveSerializer
from django.shortcuts import render, redirect
from core.models import Drive_File
from django.db.models import Q
from functools import reduce



@api_view(['GET'])
def getDrivebox(request, drivebox):
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
        return Response({"error": "Invalid drivebox."}, status=400)

    # Return files in reverse chronologial order
    files = files.order_by("-timestamp").all()
    # serializer = DriveSerializer(files, many=True)
    return Response([file.serialize() for file in files])


@api_view(['POST'])
def search(request):
    query = request.data.get("query")
    if not query:
        return Response({"error": "'query' argument should not be empty."}, status=404)

    if " " in query:
        queries = query.split(" ")
        qset1 =  reduce(operator.__or__, [Q(file__icontains=query) for query in queries])
        results = Drive_File.objects.filter(user=request.user).filter(qset1).distinct()
    else:
        results = Drive_File.objects.filter(user=request.user)\
            .filter(Q(file__icontains=query)).distinct()
    if results:
        files = results.order_by("-timestamp").all().distinct()
        serializer = DriveSerializer(files, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "No result Found"}, status=404)


@api_view(['GET', 'PUT', 'DELETE'])
def updateFile(request, file_id):

    # Query for requested email
    try:
        file = Drive_File.objects.get(user=request.user, id=file_id)
    except file.DoesNotExist:
        return Response({"error": "file not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return Response(file.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        # data = json.loads(request.body)
        data = request.data
        # if data.get("read") is not None:
        #     file.read = data["read"]
        if data.get("archived") is not None:
            file.archived = data["archived"]
        if data.get("starred") is not None:
            file.starred = data["starred"]
        if data.get("deleted") is not None:
            file.deleted = data["deleted"]
        file.save()
        serializer = DriveSerializer(file, many=False)
        return Response(serializer.data, status=204)

    elif request.method == "DELETE":
        file.delete()
        return Response({"message": "File is deleted."}, status=204)
    # Email must be via GET or PUT
    else:
        return Response({
            "error": "GET or PUT or DELETE request required."
        }, status=400)


@api_view(['POST'])
def uploadFile(request):
    if request.method == 'POST':
        file = request.FILES["file"]

        formset = Drive_File(file=file, user=request.user)
        if formset:
            formset.save()

        return Response({"message": "File Uploaded successfully."}, status=200)

    return Response({"error": "Error occur while uploading this file."}, status=401)