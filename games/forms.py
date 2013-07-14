from django import forms

from .models import GamePlay, PlayerRank


class GamePlayForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('game', 'played_at',)
