from django.shortcuts import render
import pandas as pd
from django.conf import settings
import os
import requests
from io import BytesIO

def home(request):
    # Get top 3 teams
    try:
        sheets_url = settings.TEAMS_EXCEL_URL
        if 'docs.google.com' in sheets_url:
            sheet_id = sheets_url.split('/d/')[1].split('/')[0]
            export_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx'
        else:
            export_url = sheets_url

        response = requests.get(export_url)
        response.raise_for_status()
        
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, engine='openpyxl')
        
        top_teams = []
        current_team = None
        
        for _, row in df.iterrows():
            if pd.notna(row['team']) and len(top_teams) < 3:
                top_teams.append({
                    'rank': row['place'],
                    'team_name': row['team'],
                    'team_score': row['score']
                })
        
        return render(request, "info/index.html", {'top_teams': top_teams})
    except:
        # If there's any error, just render the page without top teams
        return render(request, "info/index.html", {'top_teams': []})

def about(request):
    return render(request, "info/about.html")

def schedule(request):
    return render(request, "info/schedule.html")

def sponsors(request):
    return render(request, "info/sponsors.html")

def rules(request):
    return render(request, "info/rules.html")

def get_google_drive_file_url(sharing_url):
    # Extract file ID from sharing URL
    file_id = sharing_url.split('/d/')[1].split('/')[0]
    # Create direct download URL
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def selected_teams(request):
    # Get the Google Sheets URL from settings
    sheets_url = settings.TEAMS_EXCEL_URL
    
    try:
        # Convert Google Sheets URL to export URL
        if 'docs.google.com' in sheets_url:
            # Extract the sheet ID
            sheet_id = sheets_url.split('/d/')[1].split('/')[0]
            # Create export URL
            export_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx'
        else:
            export_url = sheets_url

        # Fetch Excel file from URL
        response = requests.get(export_url)
        response.raise_for_status()
        
        # Read Excel data from the response content
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, engine='openpyxl')
        
        # Process the data to create team-based structure
        teams_data = []
        current_team = None
        team_members = []
        
        # Iterate through rows
        for _, row in df.iterrows():
            # If team info is present (not NaN)
            if pd.notna(row['team']):
                # If there was a previous team, add it to teams_data
                if current_team is not None:
                    teams_data.append({
                        'rank': current_team['place'],
                        'team_name': current_team['team'],
                        'team_id': current_team['team id'],
                        'team_score': current_team['score'],
                        'members': team_members.copy()  # Make a copy of the members list
                    })
                
                # Start new team
                current_team = row
                team_members = []
            
            # If member info is present
            if pd.notna(row['member name']):
                team_members.append({
                    'name': row['member name'],
                    'id': row['member id'],
                    'score': row['member score']
                })
        
        # Add the last team
        if current_team is not None:
            teams_data.append({
                'rank': current_team['place'],
                'team_name': current_team['team'],
                'team_id': current_team['team id'],
                'team_score': current_team['score'],
                'members': team_members
            })
        
        # Sort teams by rank
        teams_data.sort(key=lambda x: x['rank'])
        
        # Mark selected status
        for team in teams_data:
            team['is_selected'] = team['rank'] <= 42
        
        return render(request, 'info/selected_teams.html', {
            'teams': teams_data,
            'selected_count': 42
        })
    except requests.RequestException as e:
        return render(request, 'info/selected_teams.html', {
            'teams': [], 
            'error': f"Error fetching Excel file: {str(e)}"
        })
    except Exception as e:
        return render(request, 'info/selected_teams.html', {
            'teams': [], 
            'error': f"Error processing data: {str(e)}"
        })
