from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Team

def register(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        team_leader = request.POST["team_leader"]
        team_leader_email = request.POST["team_leader_email"]
        members_count = int(request.POST["members_count"])
        password = request.POST["password"]

        # Get member details
        member_names = [request.POST[f"member_name_{i}"] for i in range(1, members_count)]
        member_emails = [request.POST[f"member_email_{i}"] for i in range(1, members_count)]

        # Check if team name exists
        if Team.objects.filter(team_name=team_name).exists():
            messages.error(request, "Team name already exists.")
        else:
            team = Team.objects.create_user(
                team_name=team_name,
                team_leader=team_leader,
                team_leader_email=team_leader_email,
                password=password,
            )
            team.member_names = ",".join(member_names)
            team.member_emails = ",".join(member_emails)
            team.save()
            messages.success(request, "Team registered successfully! Please log in.")
            return redirect("login")

    return render(request, "users/register.html")

def login_view(request):
    if request.method == "POST":
        team_name = request.POST["team_name"]
        password = request.POST["password"]

        team = authenticate(request, username=team_name, password=password)
        if team:
            login(request, team)
            messages.success(request, f"Welcome, {team.team_leader}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def profile(request):
    return render(request, "users/profile.html")

