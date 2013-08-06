from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import PlayerGroup, GroupGamePlayerRating


class PlayerGroupCreateView(CreateView):
    model = PlayerGroup


class PlayerGroupDetailView(DetailView):
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


class PlayerGroupListView(ListView):
    model = PlayerGroup
