from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from games.models import GamePlay

from ratings.models import GamePlayerRating

from .models import Player, PlayerGroup


class PlayerCreateView(CreateView):
    model = Player


class PlayerDetailView(DetailView):
    model = Player

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayerDetailView, self).get_context_data(*args, **kwargs)

        player = self.get_object()

        ctx['recently_played'] = GamePlay.objects.filter(players=player)[:5]

        ctx['ratings'] = GamePlayerRating.objects.filter(player=player)

        return ctx


class PlayerListView(ListView):
    model = Player


class PlayerGroupCreateView(CreateView):
    model = PlayerGroup
