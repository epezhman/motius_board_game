from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator


class GameStateEnum():
    Active = 'A'
    First_player = 'F'
    Second_player = 'S'
    Draw = 'D'


FIRST_PLAYER = 'X'
SECOND_PLAYER = 'O'
BOARD_SIZE = 3


class GameManager(models.Manager):
    def game_for_user(self, user):
        return super(GameManager, self).get_queryset().filter(
            Q(first_player_id=user.id) | Q(second_player_id=user.id)
        )

    def new_game(self, invitation):
        game = Game(first_player=invitation.to_user,
                    second_player=invitation.from_user,
                    next_to_play=invitation.to_user)
        return game


class Game(models.Model):
    state_choices = (
        (GameStateEnum.Active, 'Active Game'),
        (GameStateEnum.First_player, 'First Player Won'),
        (GameStateEnum.Second_player, 'Second Player Won'),
        (GameStateEnum.Draw, 'Draw Game')
    )

    start_game = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    first_player = models.ForeignKey(User, related_name="as_first_player")
    second_player = models.ForeignKey(User, related_name="as_second_player")
    next_to_play = models.ForeignKey(User, related_name="next_games")
    state = models.CharField(max_length=1, default=GameStateEnum.Active, choices=state_choices)

    objects = GameManager()

    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})

    def as_board(self):
        board = [['' for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = FIRST_PLAYER if move.by_first_player else SECOND_PLAYER
        return board

    def last_move(self):
        return self.move_set.latest()

    def is_user_move(self, user):
        return self.state == GameStateEnum.Active and self.next_to_play == user

    def is_empty(self, x, y):
        return not self.move_set.filter(x=x, y=y).exists()

    def toggle_next_player(self):
        if self.next_to_play == self.first_player:
            self.next_to_play = self.second_player
        else:
            self.next_to_play = self.first_player

    def get_state(self, last_move):
        board = self.as_board()
        x = last_move.x
        y = last_move.y
        # make this function work even if last move was not saved yet
        board[x][y] = FIRST_PLAYER if last_move.by_first_player else SECOND_PLAYER

        # check straight
        if ((board[y][0] and board[y][1] and board[y][2]) and (board[y][0] == board[y][1] == board[y][2])) or (
                    (board[0][x] and board[1][x] and board[2][x]) and
                    (board[0][x] == board[1][x] == board[2][x])):
            return GameStateEnum.First_player if last_move.by_first_player else GameStateEnum.Second_player

        # check diagonal
        if (y == x) or (abs(y - x) == 2):
            if ((board[0][0] and board[1][1] and board[2][2]) and (board[0][0] == board[1][1] == board[2][2])) or (
                        (board[0][2] and board[1][1] and board[2][0]) and
                        (board[0][2] == board[1][1] == board[2][0])):
                return GameStateEnum.First_player if last_move.by_first_player else GameStateEnum.Second_player

        if self.move_set.count() >= 9:
            return GameStateEnum.Draw
        return GameStateEnum.Active

    def create_move(self):
        return Move(game=self, by_first_player=(self.next_to_play == self.first_player))

    def update_after_move(self, move):
        self.toggle_next_player()
        self.state = self.get_state(move)


class Move(models.Model):
    x = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE - 1)])
    y = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE - 1)])
    comment = models.CharField(max_length=300, blank=True)
    game = models.ForeignKey(Game)
    by_first_player = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, )

    def player(self):
        return self.game.first_player if self.by_first_player else self.game.second_player

    def __str__(self):
        return "{0}, {1}, {2}".format(self.x, self.y, self.game)

    class Meta:
        get_latest_by = 'timestamp'


class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name="from_invitations")
    to_user = models.ForeignKey(User, related_name="to_invitations",
                                verbose_name="User to Invite")
    comment = models.CharField("Invitation Comment", max_length=300, blank=True,
                               help_text="Write some comment to the user when invitating")
    sent_time = models.DateTimeField(auto_now_add=True)
