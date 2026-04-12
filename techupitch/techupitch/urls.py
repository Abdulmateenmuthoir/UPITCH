"""
URL configuration for techupitch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

# DRF API Router Setup
from rest_framework import routers
from pitch import views as pitch_api_views

router = routers.DefaultRouter()
router.register(r'sports', pitch_api_views.SportViewSet)
router.register(r'universities', pitch_api_views.UniversityViewSet)
router.register(r'leagues', pitch_api_views.LeagueViewSet)
router.register(r'teams', pitch_api_views.TeamViewSet)
router.register(r'matches', pitch_api_views.MatchViewSet)
router.register(r'players', pitch_api_views.PlayerViewSet)
router.register(r'events', pitch_api_views.EventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('pitch/', include('pitch.urls')),
    path('', RedirectView.as_view(url='pitch/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)