from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect

from players.models import Player

from .models import Game, GamePlay, PlayerRank
from .forms import GamePlayForm


class GameCreateView(CreateView):
    model = Game


class GameDetailView(DetailView):
    model = Game


class GameListView(ListView):
    model = Game


class GamePlayCreateView(TemplateView):
    template_name = 'games/gameplay_form.html'

    def get_formset(self, instance=None, data=None):
        player_count = Player.objects.count()

        formset = inlineformset_factory(GamePlay, PlayerRank, extra=player_count, can_delete=False)

        args = ()
        kwargs = {}

        if data:
            args = (data,)

        if instance:
            kwargs = {'instance': instance}

        return formset(*args, **kwargs)

    def get_form(self, instance=None, data=None):
        args = ()
        kwargs = {}
        if data:
            args = (data,)
        if instance:
            kwargs = {'instance': instance}
        return GamePlayForm(*args, **kwargs)

    def post(self, request):
        game_play = GamePlay()
        game_play_form = self.get_form(game_play, request.POST)
        game_play_formset = self.get_formset(game_play, request.POST)

        if game_play_form.is_valid() and game_play_formset.is_valid():
            game_play = game_play_form.save()
            game_play_formset.save()

            return redirect('game_play_detail', pk=game_play.pk)

        return super(GamePlayCreateView, self).post(request)

    def get_context_data(self):
        ctx = super(GamePlayCreateView, self).get_context_data()

        ctx.update({
            'game_play_form': self.get_form(),
            'game_play_formset': self.get_formset(),
        })

        return ctx


class GamePlayDetailView(DetailView):
    model = GamePlay


class GamePlayListView(ListView):
    model = GamePlay
