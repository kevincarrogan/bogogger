from django.db import models
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField

from players.models import Player


class Game(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    min_players = models.PositiveIntegerField()
    max_players = models.PositiveIntegerField()
    is_coop = models.BooleanField(default=False, verbose_name="Co-operative")

    def get_absolute_url(self):
        return reverse('game_detail', args=(), kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name

    def has_elo_ratings(self):
        return self.min_players == 2 and self.max_players == 2


class GamePlay(models.Model):
    game = models.ForeignKey(Game)
    players = models.ManyToManyField(Player, through='PlayerRank')
    played_at = models.DateField()

    # This is only relevant for co-op games (at the moment)
    win = models.NullBooleanField()

    def get_absolute_url(self):
        return reverse('game_play_detail', args=(), kwargs={'pk': self.pk})

    def __unicode__(self):
        return u'%s - [%s]' % (self.game, u', '.join(u'%s' % player for player in self.players.all()))


class PlayerRank(models.Model):
    player = models.ForeignKey(Player)
    game_play = models.ForeignKey(GamePlay)

    # This is not relevant for co-op games (at the moment)
    rank = models.PositiveIntegerField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s. %s (%s)' % (self.rank, self.player, self.game_play)
