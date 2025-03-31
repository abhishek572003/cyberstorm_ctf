from django.urls import path
from .views import home, about, schedule, sponsors, rules, selected_teams

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('schedule/', schedule, name='schedule'),
    path('sponsors/', sponsors, name='sponsors'),
    path('rules/', rules, name='rules'),
    path('selected-teams/', selected_teams, name='selected_teams'),
]
