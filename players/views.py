from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Player


class PlayerCreateView(CreateView):
    model = Player


class PlayerDetailView(DetailView):
    model = Player


class PlayerListView(ListView):
    model = Player
