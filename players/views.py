from django.views.generic.edit import CreateView

from .models import Player


class CreatePlayerView(CreateView):
    model = Player
