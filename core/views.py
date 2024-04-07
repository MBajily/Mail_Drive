from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.csrf import csrf_exempt

# from rest_framework_simplejwt.views import TokenObtainPairView
# from .serializers import MyTokenObtainPairSerializer


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

@csrf_exempt
def is_username_exists(request):
    # data = json.loads(request.body.decode('utf-8'))
    # username = data.get('username')
    username = request

    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False


def passwordReset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            if is_username_exists(username) == False:
                return Response({"error": f"'{username}' username doesn't exist"}, status=400)

            form = PasswordResetForm({'username': username, 'site_name':"Mozal"})
            if form.is_valid():
                form.save(
                    request=request,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    # email_template_name='registration/password_reset_email.html',
                    # subject_template_name='registration/password_reset_subject.txt',
                )
                return Response(status=200)
                # return JsonResponse({'success': True, 'message': 'Password reset email has been sent.'})
            else:
                return Response(status=400)
                # return JsonResponse({'success': False, 'errors': form.errors})

        except Exception as e:
            return Response(e, status=400)

    else:
        return Response(status=400)
        # return JsonResponse({'success': False, 'message': 'Invalid request method.'})

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



def files(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "drive/files.html")

    return redirect('login')