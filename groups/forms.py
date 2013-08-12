from django import forms

from players.models import Player


class PlayerGroupPlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ('_first_name', '_last_name',)

    def __init__(self, group, *args, **kwargs):
        super(PlayerGroupPlayerForm, self).__init__(*args, **kwargs)
        self.group = group

    def save(self, *args, **kwargs):
        player = super(PlayerGroupPlayerForm, self).save(*args, **kwargs)

        self.group.players.add(player)

        return player
