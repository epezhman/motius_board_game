"""motius_board_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from tictactoe.serializers import GameViewSet
from user import urls as user_urls
from tictactoe import urls as tictactoe_urls
from django.contrib.auth import views as auth_views
from main import views as main_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include(user_urls)),
    url(r'^tictactoe/', include(tictactoe_urls)),
    url(r'^$', main_views.home, name='boradgame_home'),
    url(r'^api/', include(router.urls)),
]

urlpatterns += [
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name="boardgame_login"),
    url(r'^logout/$', auth_views.logout,
        {'next_page': 'boradgame_home'}, name="boardgame_logout"),
]
