from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new_invitation/$', views.new_invitation, name="new_invitation"),
    url(r'^accept_invitation/(?P<pk>\d+)/$', views.accept_invitation, name="accept_invitation"),
    url(r'^game/(?P<pk>\d+)/$', views.game_detail, name="game_detail"),
    url(r'^game/(?P<pk>\d+)/make_move$', views.game_make_move, name="game_make_move"),
    url(r'^game/all$', views.AllGamesView.as_view(), name="all_games"),

]
