from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path("login/", log_in, name="login"),
    path("password_reset/", password_reset, name="password_reset"),
    path('profile/', profile_page, name="profile_page"),
    path('contact/', contact, name="contact"),
    path('logout/', log_out, name="user_logout"),
]
