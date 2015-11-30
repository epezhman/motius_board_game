from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^home/$', views.user_home, name="user_home"),
    url(r'^signup/$', views.SignUpView.as_view(), name="signup")
]