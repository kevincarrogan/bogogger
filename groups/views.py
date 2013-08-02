from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import PlayerGroup


class PlayerGroupCreateView(CreateView):
    model = PlayerGroup


class PlayerGroupDetailView(DetailView):
    model = PlayerGroup


class PlayerGroupListView(ListView):
    model = PlayerGroup
