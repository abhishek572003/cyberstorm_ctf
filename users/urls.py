from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path('roll-dice/', views.roll_dice, name='roll_dice'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('select-team/', views.select_team, name='select_team'),
]
