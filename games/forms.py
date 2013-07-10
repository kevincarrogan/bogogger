from django import forms

from .models import GamePlay, PlayerRank


class GamePlayForm(forms.ModelForm):

    class Meta:
        model = GamePlay

    def save(self, *args, **kwargs):
        players = self.cleaned_data.pop('players')

        game_play = super(GamePlayForm, self).save()

        for player in players:
            PlayerRank.objects.create(game_play=game_play, player=player)

        return game_play
