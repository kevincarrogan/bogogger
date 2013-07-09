from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .models import Game, GamePlay


class GameCreateView(CreateView):
    model = Game


class GameDetailView(DetailView):
    model = Game


class GamePlayCreateView(CreateView):
    model = GamePlay
