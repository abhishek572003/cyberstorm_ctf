from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path('roll-dice/', views.roll_dice, name='roll_dice'),
]
