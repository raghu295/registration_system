import email
from os import name
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm
from .models import Profile, Contact, User
from django.contrib.auth.models import User
from .helper import save_file
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import re

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
       first_name = request.POST.get("first_name")
       last_name = request.POST.get("last_name")
       email_id = request.POST.get("email")
       password = request.POST.get("password")
       confirm_password = request.POST.get("confirm_password")
       
       
       if password != confirm_password:
           messages.error(request, "Password and Confirm password does not match")
           return redirect("register")
       
       if not is_valid_password(password):
            messages.error(
                request,
                "Password must be at least 6 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character."
            )
            return redirect("register")

       if User.objects.filter(email=email_id).exists():
           messages.error(request, message="Email already exists")
           return redirect("register")

        # insert profile to database
       user_data = {"username": email_id, "email": email_id, "password": password}
       user = User.objects.create(**user_data)
       user.set_password(password)
       user.save()
       profile_data = {"user": user, "firstname": first_name, "lastname": last_name}
       profile = Profile.objects.create(**profile_data)
       return redirect("login")
        
    return render(request, 'register.html', {'form': form})



def home(request):
    message = "Hello Everyone Welcome to my Registration Page"
    context = {"message": message}
    return render(request, "home.html")


def log_in(request):
    if request.method == "POST":
        email_id = request.POST.get("email")
        password = request.POST.get("password")
       
        # check if email exist in database
        if not User.objects.filter(email = email_id).exists():
            messages.error(request, message="Email does not exists")
            return redirect("login")
        # check if email or password is correct
        user_query = User.objects.get(email=email_id)
        username = None
        if user_query:
            username = user_query.username     # get user from user table
        user = authenticate(request, username =username, password= password)
        if user is not None:
            login(request, user)
            profile_pic = None
            if Profile.objects.filter(user__email=request.user.email).exists():
                profile_pic = Profile.objects.get(user__email=request.user.email).profile_image
            request.session["profile_pic"] = profile_pic
            return redirect("home")

        else:
            messages.error(request, message="Email or Password is incorrect")
            return redirect("login")
    return render(request, "login.html")


def password_reset(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            messages.success(request, "Your password has been successfully changed")
            return redirect('login')
        
    return render(request, 'password_reset.html')


@login_required
def profile_page(request):
    # get value on session
    print("request.session:", request.session.get("blog"))
    profile = {}
    if Profile.objects.filter(user__email=request.user.email).exists():
        profile = Profile.objects.get(user__email=request.user.email)
        if request.method == "POST":
            contact = request.POST.get("contact")
            address = request.POST.get("address")
            profile_image = request.FILES.get("profile_image")
            if profile_image:
                profile_image_url = save_file(request, profile_image)
                profile.profile_image = profile_image_url
            if contact:
                profile.contact = contact
            if address:
                profile.address = address
            profile.save()
            messages.info(request, message="Profile updated Successfully")
            return redirect("profile_page")
    context = {"profile": profile}
    return render(request, "profile.html", context)



def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name:
            contact.name = name

        if email:
            contact.email = email

        if message:
            contact.message = message


        # Save the contact data to the database
        contact_data = {"name": name, "email": email, "message": message}
        print(contact_data)
        Contact.objects.create(**contact_data)
        messages.info(request, message="We have received your message and will get back to you shortly")
        return redirect("contact")

    # get value on session
    return render(request, "contact.html")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login")


def is_valid_password(password):
    """
    Validate password strength.
    Password must be at least 6 characters long,
    contain at least one uppercase letter, one lowercase letter,
    one digit, and one special character.
    """
    if (
        len(password) >= 6
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in r"!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for c in password)
    ):
        return True
    return False
