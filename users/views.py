import json
import logging
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from google.auth.transport import requests
from google.oauth2 import id_token
from django.db.models import Q

from .models import Team, TeamMember

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
            
            # Basic validation
            if not team_name or not password:
                messages.error(request, 'Team name and password are required!')
                return render(request, 'users/register.html', context)

            # Validate passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'users/register.html', context)

            # Get leader details
            leader_name = request.POST.get('member_name_0')
            leader_email = request.POST.get('member_email_0')
            leader_phone = request.POST.get('member_phone_0')
            
            if not all([leader_name, leader_email, leader_phone]):
                messages.error(request, 'Team leader details are required!')
                return render(request, 'users/register.html', context)

            # Check if team name or email already exists
            if Team.objects.filter(Q(team_name=team_name) | Q(team_leader_email=leader_email)).exists():
                messages.error(request, 'Team name or leader email already exists!')
                return render(request, 'users/register.html', context)

            # Create team with validated data
            team = Team.objects.create_user(
                team_name=team_name,
                team_leader=leader_name,
                team_leader_email=leader_email,
                password=password
            )

            # Update additional fields
            team.phone_number = leader_phone
            team.is_professional = request.POST.get('is_professional') == 'on'
            
            # Handle member data
            member_names = []
            member_emails = []
            member_phones = []
            
            members_count = int(request.POST.get('members_count', 1))
            for i in range(members_count):
                name = request.POST.get(f'member_name_{i}')
                email = request.POST.get(f'member_email_{i}')
                phone = request.POST.get(f'member_phone_{i}')
                if name and email and phone:
                    member_names.append(name)
                    member_emails.append(email)
                    member_phones.append(phone)

            team.member_names = ','.join(member_names)
            team.member_emails = ','.join(member_emails)
            team.member_phones = ','.join(member_phones)
            team.save()

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'users/register.html', context)

    return render(request, 'users/register.html', context)


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"].strip().lower()
        
        # Generate a 6-digit verification code
        verification_code = str(random.randint(100000, 999999))
        
        # Store the code in session
        request.session['verification_code'] = verification_code
        request.session['email'] = email
        
        # Send email
        try:
            # Render the email template
            html_content = render_to_string('users/email_template.html', {
                'verification_code': verification_code
            })
            text_content = strip_tags(html_content)  # Create plain text version

            # Create the email
            email_message = EmailMultiAlternatives(
                subject='Cyberstorm Verification Code',  # Changed subject
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )

            # Attach HTML content
            email_message.attach_alternative(html_content, "text/html")

            # Send email
            email_message.send()
            messages.success(request, 'Verification code sent to your email!')

            return render(request, 'users/verify_email.html', {
                'verification_sent': True,
                'email': email
            })

        except Exception as primary_error:
            logger.error(f"Primary email failed: {str(primary_error)}")

    return render(request, "users/login.html")


def logout_view(request):
    # Clear any session data
    request.session.flush()
    # Perform Django logout
    logout(request)
    messages.success(request, "Successfully logged out!")
    # Redirect to login page
    return redirect('login')


@login_required
def profile(request):
    # Get all team members for the current user's team
    team_members = TeamMember.objects.filter(team=request.user)

    return render(request, 'users/profile.html', {
        'team_members': team_members
    })


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


@ensure_csrf_cookie
def google_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'users/google_login.html')




def verify_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Generate a 6-digit verification code
        verification_code = str(random.randint(100000, 999999))
        
        # Store the code in session
        request.session['verification_code'] = verification_code
        request.session['email'] = email
        
        try:
            # Render the email template
            html_content = render_to_string('users/email_template.html', {
                'verification_code': verification_code
            })
            text_content = strip_tags(html_content)  # Create plain text version
            
            # Create the email
            email_message = EmailMultiAlternatives(
                subject='Cyberstorm Verification Code',  # Changed subject
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            
            # Attach HTML content
            email_message.attach_alternative(html_content, "text/html")
            
            # Send email
            email_message.send()
            messages.success(request, 'Verification code sent to your email!')
            
        except Exception as primary_error:
            logger.error(f"Primary email failed: {str(primary_error)}")
        
        return render(request, 'users/verify_email.html', {
            'verification_sent': True,
            'email': email
        })
            
    return render(request, 'users/verify_email.html', {'verification_sent': False})

def verify_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        email = request.POST.get('email')
        stored_code = request.session.get('verification_code')
        stored_email = request.session.get('email')
        
        if entered_code == stored_code and email == stored_email:
            # Find all teams associated with this email
            teams = []
            
            # Check TeamMember table
            team_members = TeamMember.objects.filter(email=email)
            for member in team_members:
                if member.team not in teams:
                    teams.append(member.team)
            
            # Check Team table for team leaders
            leader_teams = Team.objects.filter(team_leader_email=email)
            for team in leader_teams:
                if team not in teams:
                    teams.append(team)
            
            if len(teams) == 0:
                messages.error(request, 'No team found with this email.')
                return render(request, 'users/verify_email.html', {
                    'verification_sent': True,
                    'email': email
                })
            elif len(teams) == 1:
                # If only one team found, log them in
                auth_login(request, teams[0])
                messages.success(request, f'Welcome back, {teams[0].team_name}!')
                return redirect('profile')
            else:
                # If multiple teams found, let user choose
                return render(request, 'users/select_team.html', {
                    'teams': teams,
                    'email': email
                })
        else:
            messages.error(request, 'Invalid verification code.')
        
    return render(request, 'users/verify_email.html', {
        'verification_sent': True,
        'email': request.POST.get('email')
    })


def select_team(request):
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        email = request.POST.get('email')
        
        try:
            team = Team.objects.get(id=team_id)
            # Verify the email is associated with this team
            is_member = TeamMember.objects.filter(team=team, email=email).exists()
            is_leader = team.team_leader_email == email
            
            if is_member or is_leader:
                auth_login(request, team)
                messages.success(request, f'Welcome back, {team.team_name}!')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid team selection.')
        except Team.DoesNotExist:
            messages.error(request, 'Team not found.')
    
    return redirect('login')

