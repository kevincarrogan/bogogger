from django import forms
from django.forms.models import BaseInlineFormSet

from .models import GamePlay, PlayerRank


class GamePlayForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('game', 'played_at',)


class GamePlayFromGameForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('played_at',)


class GamePlayFromCoopGameForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('played_at', 'win',)


class PlayerRankForm(forms.ModelForm):

    class Meta:
        model = PlayerRank


class PlayerRankCoopGameForm(forms.ModelForm):

    class Meta:
        model = PlayerRank
        fields = ('player',)


class PlayerRankFormset(BaseInlineFormSet):

    def clean(self, *args, **kwargs):
        instance = self.instance
        game = self.instance.game
        min_players = game.min_players

        if len(self.forms) < min_players:
            raise forms.ValidationError('This game requires at least %d players to have played' % min_players)

        return super(PlayerRankFormset, self).clean(*args, **kwargs)
