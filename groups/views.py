from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.http import Http404

from braces.views import LoginRequiredMixin

from players.models import Player

from games.views import BaseGameListView, GameCreateView
from authorisation.views import SignUpView

from .models import PlayerGroup, GroupGamePlayerRating, PlayerGroupInvite
from .forms import PlayerGroupForm, PlayerGroupPlayerForm, PlayerGroupInviteForm


class PlayerGroupCreateView(LoginRequiredMixin, CreateView):
    model = PlayerGroup
    form_class = PlayerGroupForm

    def form_valid(self, form):
        resp = super(PlayerGroupCreateView, self).form_valid(form)

        player = self.request.user.player_set.all()[0]
        player_group = form.instance

        player_group.players.add(player)

        return resp


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

    def get_queryset(self):
        queryset = super(PlayerGroupListView, self).get_queryset()

        user = self.request.user

        if not user.has_perm('view_all_groups'):
            player = user.player_set.all()[0]
            queryset = queryset.filter(players=player)

        return queryset


class PlayerGroupPlayerAddView(LoginRequiredMixin, CreateView):
    model = Player
    form_class = PlayerGroupPlayerForm

    def get_form_kwargs(self):
        kwargs = super(PlayerGroupPlayerAddView, self).get_form_kwargs()
        group_slug = self.kwargs['slug']
        group = PlayerGroup.objects.get(slug=group_slug)
        kwargs['group'] = group
        return kwargs


class PlayerGroupGameListView(BaseGameListView):
    template_name = 'groups/playergroup_game_list.html'

    def get_object(self):
        return PlayerGroup.objects.get(slug=self.kwargs['slug'])

    def get_queryset(self):
        queryset = super(PlayerGroupGameListView, self).get_queryset()

        player_group = self.get_object()
        queryset = queryset.filter(playergroup=player_group)

        return queryset

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayerGroupGameListView, self).get_context_data(*args, **kwargs)

        ctx['group'] = self.get_object()

        return ctx


class PlayerGroupGameCreateView(GameCreateView):
    template_name = 'groups/playergroup_game_create.html'

    def get_object(self):
        return PlayerGroup.objects.get(slug=self.kwargs['slug'])

    def form_valid(self, form):
        resp = super(PlayerGroupGameCreateView, self).form_valid(form)

        player_group = self.get_object()
        player_group.games.add(form.instance)

        return resp


class PlayerGroupPlayerInviteView(LoginRequiredMixin, CreateView):
    model = PlayerGroupInvite
    form_class = PlayerGroupInviteForm

    def get_form_kwargs(self):
        kwargs = super(PlayerGroupPlayerInviteView, self).get_form_kwargs()

        kwargs['group'] = self.get_object()

        return kwargs

    def get_object(self):
        return PlayerGroup.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('player_list')

    def form_valid(self, form):
        resp = super(PlayerGroupPlayerInviteView, self).form_valid(form)

        invite = form.instance
        email = EmailMessage(
            'Boggoger: Invite',
            'You have been invited to join "%s" on bogogger.com.\n\n'
            'To accept this request visit: http://www.bogogger.com%s' % (invite.group, reverse('player_group_invite_accept', args=(invite.group.slug, invite.hash,))),
            'info@bogogger.com',
            [invite.email],
        )
        email.send()

        return resp


class PlayerGroupPlayerInviteAcceptView(SignUpView):

    def get(self, request, slug, hash):
        try:
            group = PlayerGroup.objects.get(slug=slug)
        except PlayerGroup.DoesNotExist:
            raise Http404

        try:
            invite = PlayerGroupInvite.objects.get(
                group=group,
                hash=hash,
            )
        except PlayerGroupInvite.DoesNotExist:
            raise Http404

        return super(PlayerGroupPlayerInviteAcceptView, self).get(request)

    def get_form_kwargs(self):
        kwargs = super(PlayerGroupPlayerInviteAcceptView, self).get_form_kwargs()

        invite = PlayerGroupInvite.objects.get(
            group__slug=self.kwargs['slug'],
            hash=self.kwargs['hash'],
        )

        kwargs['initial']['email'] = invite.email

        return kwargs

    def form_valid(self, form):
        resp = super(PlayerGroupPlayerInviteAcceptView, self).form_valid(form)

        player = form.instance.player_set.all()[0]
        group = PlayerGroup.objects.get(slug=self.kwargs['slug'])
        group.players.add(player)

        return resp
