import uuid

from django import forms

from players.models import Player

from .models import PlayerGroupInvite


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


class PlayerGroupInviteForm(forms.ModelForm):

    class Meta:
        model = PlayerGroupInvite
        fields = ('email',)

    def __init__(self, group, *args, **kwargs):
        self.group = group
        super(PlayerGroupInviteForm, self).__init__(*args, **kwargs)

    def save(self):
        self.instance.group = self.group
        self.instance.hash = uuid.uuid4().hex

        return super(PlayerGroupInviteForm, self).save()
