from django.urls import path
from .views import home, about, schedule, sponsors, rules

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('schedule/', schedule, name='schedule'),
    path('sponsors/', sponsors, name='sponsors'),
    path('rules/', rules, name='rules'),
]
