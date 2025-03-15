from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Team, TeamMember
from django.contrib.auth.decorators import login_required
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import random
from django.conf import settings
from django.urls import reverse

logger = logging.getLogger(__name__)

def get_base_context():
    return {
        'settings': settings,
        'social_links': settings.SOCIAL_LINKS,
        'meta': settings.SITE_META,
        'whatsapp_sponsor_number': settings.WHATSAPP_SPONSOR_NUMBER,
        'whatsapp_sponsor_text': settings.WHATSAPP_SPONSOR_TEXT,
        'whatsapp_footer_number': settings.WHATSAPP_FOOTER_NUMBER,
        'whatsapp_footer_text': settings.WHATSAPP_FOOTER_TEXT,
        'contact_email': settings.CONTACT_EMAIL,
        'cc_email': settings.CC_EMAIL
    }

def register(request):
    context = get_base_context()
    if request.method == 'POST':
        try:
            # Get form data
            team_name = request.POST.get('team_name')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validate passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'users/register.html', context)

            is_professional = request.POST.get('is_professional', False) == 'on'
            members_count = int(request.POST.get('members_count', 1))

            # Get leader details
            leader_name = request.POST.get('member_name_0')
            leader_email = request.POST.get('member_email_0')
            leader_phone = request.POST.get('member_phone_0')

            if not all([leader_name, leader_email, leader_phone]):
                messages.error(request, 'Team leader details are required!')
                return render(request, 'users/register.html', context)

            # Check if team name already exists
            if Team.objects.filter(team_name=team_name).exists():
                messages.error(request, 'Team name already exists!')
                return render(request, 'users/register.html', context)

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

            # Auto login after registration
            login(request, team)
            messages.success(request, 'Registration successful! Welcome aboard!')
            return redirect('profile')

        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'users/register.html', context)

    return render(request, 'users/register.html', context)

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

@login_required
def profile(request):
    try:
        context = {
            'user': request.user,
            'team_members': request.user.members.all() if hasattr(request.user, 'members') else []
        }
        return render(request, 'users/profile.html', context)
    except Exception as e:
        logger.error(f"Error in profile view: {str(e)}")
        # For debugging only - remove in production
        raise e

@require_POST
def roll_dice(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not authenticated'})
    
    try:
        roll_value = random.randint(1, 6)
        bounty_increase = roll_value * 0.1  # Small fraction of points
        
        # Update user's bounty
        request.user.points = (request.user.points or 0) + bounty_increase
        request.user.save()
        
        return JsonResponse({
            'success': True,
            'roll_value': roll_value,
            'new_bounty': round(request.user.points, 1)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def index(request):
    context = get_base_context()
    return render(request, 'info/index.html', context)

def about(request):
    context = get_base_context()
    return render(request, 'info/about.html', context)

def schedule(request):
    context = get_base_context()
    return render(request, 'info/schedule.html', context)

def rules(request):
    context = get_base_context()
    return render(request, 'info/rules.html', context)

def sponsors(request):
    context = get_base_context()
    return render(request, 'info/sponsors.html', context)

def password_reset(request):
    context = get_base_context()
    
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        
        # Validate passwords match
        if new_password != confirm_new_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/password_reset.html', context)
        
        # Try to find the team
        try:
            team = Team.objects.get(team_name=team_name)
            
            # Verify team leader's email and phone
            team_leader = TeamMember.objects.filter(team=team, is_leader=True).first()
            
            if not team_leader:
                messages.error(request, 'Team leader information not found.')
                return render(request, 'users/password_reset.html', context)
            
            if team_leader.email != email or team_leader.phone != phone:
                messages.error(request, 'The provided information does not match our records.')
                return render(request, 'users/password_reset.html', context)
            
            # Update the password
            team.set_password(new_password)
            team.save()
            
            messages.success(request, 'Password has been reset successfully!')
            return redirect('password_reset_done')
            
        except Team.DoesNotExist:
            messages.error(request, 'Team not found.')
            return render(request, 'users/password_reset.html', context)
        
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'users/password_reset.html', context)
    
    return render(request, 'users/password_reset.html', context)

def password_reset_done(request):
    context = get_base_context()
    return render(request, 'users/password_reset_done.html', context)

