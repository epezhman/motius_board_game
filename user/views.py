from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from tictactoe.models import Game
from tictactoe.models import GameStateEnum


@login_required
def user_home(request):
    my_games = Game.objects.game_for_user(request.user)
    active_games = my_games.filter(state=GameStateEnum.Active)
    finished_games = my_games.exclude(state=GameStateEnum.Active)
    waiting_games = active_games.filter(next_to_play=request.user)
    other_games = active_games.exclude(next_to_play=request.user)

    invitations = request.user.to_invitations.all()

    context = {
        'other_games': other_games,
        'finished_games': finished_games,
        'waiting_games': waiting_games,
        'invitations': invitations
    }

    return render(request, "user/home.html", context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "user/signup.html"
    success_url = reverse_lazy('user_home')