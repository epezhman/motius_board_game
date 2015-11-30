from django.contrib import admin
from .models import Game, Move


class InlineMove(admin.TabularInline):
    model = Move


class GameAdmin(admin.ModelAdmin):
    list_display = ['first_player', 'second_player', 'start_game']
    search_fields = ['start_game']
    list_filter = ['first_player']
    inlines = [InlineMove]


admin.site.register(Game, GameAdmin)

admin.site.register(Move)
