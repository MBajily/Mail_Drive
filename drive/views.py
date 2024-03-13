from django.shortcuts import render

# Create your views here.
def files(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "drive/files.html")