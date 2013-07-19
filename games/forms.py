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
