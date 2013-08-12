from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from braces.views import LoginRequiredMixin

from players.models import Player

from .models import PlayerGroup, GroupGamePlayerRating
from .forms import PlayerGroupPlayerForm


class PlayerGroupCreateView(LoginRequiredMixin, CreateView):
    model = PlayerGroup


class PlayerGroupDetailView(LoginRequiredMixin, DetailView):
    model = PlayerGroup

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayerGroupDetailView, self).get_context_data(*args, **kwargs)

        leaderboards = []

        group = self.get_object()

        for game in group.games.all():
            leaderboards.append(
                (game, GroupGamePlayerRating.objects.filter(game=game, group=group).order_by('-rating__rating'),),
            )

        ctx['leaderboards'] = leaderboards

        return ctx


class PlayerGroupListView(LoginRequiredMixin, ListView):
    model = PlayerGroup


class PlayerGroupPlayerAddView(LoginRequiredMixin, CreateView):
    model = Player
    form_class = PlayerGroupPlayerForm

    def get_form_kwargs(self):
        kwargs = super(PlayerGroupPlayerAddView, self).get_form_kwargs()
        group_slug = self.kwargs['slug']
        group = PlayerGroup.objects.get(slug=group_slug)
        kwargs['group'] = group
        return kwargs
