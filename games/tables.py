import django_tables2 as tables
from django_tables2.utils import A

from django.core.urlresolvers import reverse

from .models import Game
from ratings.models import GamePlayerRating


class EmptyTableMixin(object):

    def __init__(self, *args, **kwargs):
        super(EmptyTableMixin, self).__init__(*args, **kwargs)
        if not len(self.rows):
            self.attrs['class'] = 'empty-table'

    @property
    def model_verbose_plural_name(self):
        model = self._meta.model
        return model._meta.verbose_name_plural


class GameTable(EmptyTableMixin, tables.Table):
    name = tables.LinkColumn('game_detail', args=[A('slug')])

    class Meta:
        model = Game
        fields = ('name', 'number_of_players',)

    @property
    def new_model_url(self):
        return reverse('game_create')


class GameLeaderboardTable(EmptyTableMixin, tables.Table):
    player = tables.LinkColumn(
        'player_detail',
        args=[A('player.slug')]
    )

    class Meta:
        model = GamePlayerRating
        fields = ('player', 'rating.rating',)
