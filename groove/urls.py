"""groove URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from grooveapi.views import register_user, login_user
from grooveapi.views import StageView

from rest_framework import routers
from grooveapi.views.artist import ArtistView
from grooveapi.views.my_lineup import MyLineupView
from grooveapi.views.profile import ProfileView

from grooveapi.views.show import ShowView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'stages', StageView, 'stage')
router.register(r'shows', ShowView, 'show')
router.register(r'artists', ArtistView, 'artist')
router.register(r'myshows', MyLineupView, 'myshow')
router.register(r'profiles', ProfileView, 'profile')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
