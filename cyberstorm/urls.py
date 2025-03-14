# team_portal/urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Create Sitemap class
class CyberstormSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['home', 'about', 'schedule', 'sponsors', 'rules', 'register']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'static': CyberstormSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('info.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt',
         TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
         name="robots.txt"),
]
