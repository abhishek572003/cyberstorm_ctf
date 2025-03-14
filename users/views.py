from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Team

def register(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        is_professional = request.POST.get("is_professional") == "on"
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "users/register.html")

        # Get the first member's details (individual or team leader)
        member_names = [request.POST["member_name_0"]]
        member_emails = [request.POST["member_email_0"]]
        member_phones = [request.POST["member_phone_0"]]

        # If team registration, get other members' details
        members_count = int(request.POST.get("members_count", 1))
        if members_count > 1:
            for i in range(1, members_count):
                member_names.append(request.POST[f"member_name_{i}"])
                member_emails.append(request.POST[f"member_email_{i}"])
                member_phones.append(request.POST[f"member_phone_{i}"])

        if Team.objects.filter(team_name=team_name).exists():
            messages.error(request, "Team name already exists.")
        else:
            team = Team.objects.create_user(
                team_name=team_name,
                team_leader=member_names[0],
                team_leader_email=member_emails[0],
                password=password,
            )
            team.is_professional = is_professional
            team.member_names = ",".join(member_names[1:])
            team.member_emails = ",".join(member_emails[1:])
            team.member_phones = ",".join(member_phones)
            team.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")

    return render(request, "users/register.html")

def login_view(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        password = request.POST["password"]

        team = authenticate(request, username=team_name, password=password)
        if team:
            login(request, team)
            messages.success(request, "Login Successful")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def profile(request):
    return render(request, "users/profile.html")

