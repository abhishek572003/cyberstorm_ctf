from django.shortcuts import render

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if maintenance mode is enabled
        from django.conf import settings
        
        if settings.MAINTENANCE_MODE:
            # Allow superusers to still access the site
            if not request.user.is_authenticated or not request.user.is_superuser:
                # Exclude admin paths
                if not request.path.startswith('/admin'):
                    return render(request, 'maintenance.html')
        
        return self.get_response(request)