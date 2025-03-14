from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Team, TeamMember

def register(request):
    if request.method == 'POST':
        try:
            # Get form data
            team_name = request.POST.get('team_name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validate passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'users/register.html')

            is_professional = request.POST.get('is_professional', False) == 'on'
            members_count = int(request.POST.get('members_count', 1))

            # Get leader details
            leader_name = request.POST.get('member_name_0')
            leader_email = request.POST.get('member_email_0')
            leader_phone = request.POST.get('member_phone_0')

            if not all([leader_name, leader_email, leader_phone]):
                messages.error(request, 'Team leader details are required!')
                return render(request, 'users/register.html')

            # Check if team name already exists
            if Team.objects.filter(team_name=team_name).exists():
                messages.error(request, 'Team name already exists!')
                return render(request, 'users/register.html')

            # Create team
            team = Team.objects.create_user(
                team_name=team_name,
                team_leader=leader_name,
                team_leader_email=leader_email,
                password=password
            )
            
            # Update additional team fields
            team.is_professional = is_professional
            team.phone_number = leader_phone
            team.save()

            # Store member details
            member_names = []
            member_emails = []
            member_phones = []

            # Create team members
            for i in range(members_count):
                name = request.POST.get(f'member_name_{i}')
                email = request.POST.get(f'member_email_{i}')
                phone = request.POST.get(f'member_phone_{i}')
                
                if name and email and phone:
                    TeamMember.objects.create(
                        team=team,
                        name=name,
                        email=email,
                        phone=phone,
                        is_leader=(i == 0)
                    )
                    
                    if i > 0:  # Skip leader as they're already stored
                        member_names.append(name)
                        member_emails.append(email)
                        member_phones.append(phone)

            # Update team with member lists
            team.member_names = ','.join(member_names)
            team.member_emails = ','.join(member_emails)
            team.member_phones = ','.join(member_phones)
            team.save()

            # Log in the new team
            login(request, team)
            messages.success(request, 'Team registered successfully!')
            return redirect('home')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')

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

