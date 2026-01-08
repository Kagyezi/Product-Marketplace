from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.

def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("internal-products")
        else:
            error = "Invalid credentials"

    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("home")
