from django.core.exceptions import ValidationError
from django.forms import ModelForm
from tictactoe.models import Invitation, Move, GameStateEnum


class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ['from_user']


class MoveForm(ModelForm):

    def clean(self):
            game = self.instance.game
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            if not game or not game.state == GameStateEnum.Active or not game.is_empty(x, y):
                raise ValidationError("This Move is Illegal")
            return self.cleaned_data


    class Meta:
        model = Move
        exclude = ['game', 'by_first_player', 'comment']


