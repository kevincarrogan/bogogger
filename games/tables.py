import django_tables2 as tables
from django_tables2.utils import A

from .models import Game


class GameTable(tables.Table):
    name = tables.LinkColumn('game_detail', args=[A('slug')])

    class Meta:
        model = Game
        fields = ('name', 'number_of_players',)

    def __init__(self, *args, **kwargs):
        super(GameTable, self).__init__(*args, **kwargs)
        if not len(self.rows):
            self.attrs['class'] = 'empty-table'
