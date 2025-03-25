from django.urls import path, include

urlpatterns = [
    # ... other URLs ...
    path('', include('your_app_name.urls')),  # Replace 'your_app_name' with your actual app name
] 