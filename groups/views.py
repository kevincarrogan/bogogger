from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .models import PlayerGroup


class PlayerGroupCreateView(CreateView):
    model = PlayerGroup


class PlayerGroupDetailView(DetailView):
    model = PlayerGroup
