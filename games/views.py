from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView, BaseDetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect

from players.models import Player
from ratings.models import GamePlayerRating

from .models import Game, GamePlay, PlayerRank
from .forms import GamePlayForm, GamePlayFromGameForm, GamePlayFromCoopGameForm, PlayerRankForm, PlayerRankCoopGameForm, PlayerRankFormset


class GameCreateView(CreateView):
    model = Game


class GameDetailView(DetailView):
    model = Game

    def get_context_data(self, object):
        ctx = super(GameDetailView, self).get_context_data()

        ratings = GamePlayerRating.objects.filter(game=self.get_object())
        ratings = ratings.order_by('-rating__rating')
        ratings = ratings[:10]

        ctx['ratings'] = ratings

        return ctx


class GameListView(ListView):
    model = Game


class GameUpdateView(UpdateView):
    model = Game


class GamePlayCreateView(TemplateView):
    template_name = 'games/gameplay_form.html'

    def get_formset(self, instance=None, data=None):
        player_count = Player.objects.count()

        formset = inlineformset_factory(
            GamePlay,
            PlayerRank,
            form=PlayerRankForm,
            extra=player_count,
            can_delete=False,
        )

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

        return self.render_to_response(self.get_context_data(form=game_play_form, formset=game_play_formset))

    def get_context_data(self, form=None, formset=None):
        ctx = super(GamePlayCreateView, self).get_context_data()

        if not form:
            form = self.get_form()

        if not formset:
            formset = self.get_formset()

        ctx.update({
            'game_play_form': form,
            'game_play_formset': formset,
        })

        return ctx


class GamePlayCreateFromGameView(BaseDetailView, TemplateView):
    model = Game
    template_name = 'games/gameplay_from_game_form.html'

    def get_formset(self, instance=None, data=None):
        player_count = Player.objects.count()

        game = self.get_object()

        if game.is_coop:
            player_rank_form_class = PlayerRankCoopGameForm
        else:
            player_rank_form_class = PlayerRankForm

        formset = inlineformset_factory(
            GamePlay,
            PlayerRank,
            form=player_rank_form_class,
            formset=PlayerRankFormset,
            extra=player_count,
            can_delete=False,
        )

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

        game = self.get_object()

        if game.is_coop:
            return GamePlayFromCoopGameForm(*args, **kwargs)

        return GamePlayFromGameForm(*args, **kwargs)

    def post(self, request, slug):
        game_play = GamePlay(game=self.get_object())
        game_play_form = self.get_form(game_play, request.POST)
        game_play_formset = self.get_formset(game_play, request.POST)

        # Doing this here so that we can run both and display all errors
        # In an if statement this may shortcircuit.
        game_play_form_is_valid = game_play_form.is_valid()
        game_play_formset_is_valid = game_play_formset.is_valid()

        if game_play_form_is_valid and game_play_formset_is_valid:
            game_play = game_play_form.save()
            game_play_formset.save()

            return redirect('game_play_detail', pk=game_play.pk)

        self.object = self.get_object()

        return self.render_to_response(self.get_context_data(object=self.get_object(), form=game_play_form, formset=game_play_formset))

    def get_context_data(self, object, form=None, formset=None):
        ctx = super(GamePlayCreateFromGameView, self).get_context_data()

        if not form:
            form = self.get_form()

        if not formset:
            formset = self.get_formset()

        ctx.update({
            'game_play_form': form,
            'game_play_formset': formset,
        })

        return ctx


class GamePlayUpdateView(TemplateView):
    template_name = 'games/gameplay_form.html'

    def get_formset(self, instance, data=None):
        player_count = Player.objects.count()

        formset = inlineformset_factory(
            GamePlay,
            PlayerRank,
            form=PlayerRankForm,
            extra=player_count,
            can_delete=False,
        )

        args = ()
        kwargs = {}

        if data:
            args = (data,)

        if instance:
            kwargs = {'instance': instance}

        return formset(*args, **kwargs)

    def get_form(self, instance, data=None):
        args = ()
        kwargs = {}
        if data:
            args = (data,)
        if instance:
            kwargs = {'instance': instance}
        return GamePlayForm(*args, **kwargs)

    def get(self, request, pk):
        game_play = GamePlay.objects.get(pk=pk)

        game_play_form = self.get_form(game_play)
        game_play_formset = self.get_formset(game_play)

        return self.render_to_response(self.get_context_data(game_play=game_play, form=game_play_form, formset=game_play_formset))

    def post(self, request, pk):
        game_play = GamePlay.objects.get(pk=pk)
        game_play_form = self.get_form(game_play, request.POST)
        game_play_formset = self.get_formset(game_play, request.POST)

        if game_play_form.is_valid() and game_play_formset.is_valid():
            game_play = game_play_form.save()
            game_play_formset.save()

            return redirect('game_play_detail', pk=game_play.pk)

        return self.render_to_response(self.get_context_data(game_play=game_play, form=game_play_form, formset=game_play_formset))

    def get_context_data(self, game_play, form, formset):
        ctx = super(GamePlayUpdateView, self).get_context_data()

        ctx.update({
            'game_play': game_play,
            'game_play_form': form,
            'game_play_formset': formset,
        })

        return ctx


class GamePlayDetailView(DetailView):
    model = GamePlay


class GamePlayListView(ListView):
    model = GamePlay
