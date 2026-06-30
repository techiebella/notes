from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# -------------------------
# Home Page
# -------------------------
def home(request):
    return render(request, "home.html")


# -------------------------
# User Registration
# -------------------------
def signup_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check empty fields
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("signup")

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        # Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        # Password confirmation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # Password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("signup")

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "accounts/signup.html")


# -------------------------
# User Login
# -------------------------
def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# -------------------------
# User Logout
# -------------------------
def logout_view(request):

    logout(request)

    messages.success(request, "You have been logged out successfully.")

    return redirect("home")