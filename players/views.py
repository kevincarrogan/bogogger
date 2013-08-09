from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin

from games.models import GamePlay

from ratings.models import GamePlayerRating

from .models import Player


class PlayerCreateView(LoginRequiredMixin, CreateView):
    model = Player


class PlayerDetailView(LoginRequiredMixin, DetailView):
    model = Player

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayerDetailView, self).get_context_data(*args, **kwargs)

        player = self.get_object()

        ctx['recently_played'] = GamePlay.objects.filter(players=player)[:5]

        ctx['ratings'] = GamePlayerRating.objects.filter(player=player)

        return ctx


class PlayerListView(LoginRequiredMixin, ListView):
    model = Player
