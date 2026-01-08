from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import User, Business

# Create your views here.

def signup_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if role not in ["ADMIN", "VIEWER"]:
            error = "Invalid role selected"
        elif User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            # Create a business automatically for Admins
            business = None
            if role == "ADMIN":
                business = Business.objects.create(name=f"{username}'s Business")

            user = User.objects.create_user(
                username=username,
                password=password,
                role=role,
                business=business
            )

            login(request, user)

            if role == "ADMIN":
                return redirect("admin-dashboard")
            else:
                return redirect("viewer-products")

    return render(request, "signup.html", {"error": error})

def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        selected_role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if not user:
            error = "Invalid credentials"
        elif user.role != selected_role:
            error = "Role does not match account role"
        else:
            login(request, user)

            if user.role == "ADMIN":
                return redirect("admin-dashboard")
            else:
                return redirect("viewer-products")

    return render(request, "login.html", {"error": error})



def logout_view(request):
    logout(request)
    return redirect("/login")
