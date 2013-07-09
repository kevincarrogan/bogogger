from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Game


class GameCreateView(CreateView):
    model = Game


class GameDetailView(DetailView):
    model = Game


class GameListView(ListView):
    model = Game
