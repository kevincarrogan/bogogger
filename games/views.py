from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .models import Game


class GameCreateView(CreateView):
    model = Game


class GameDetailView(DetailView):
    model = Game
