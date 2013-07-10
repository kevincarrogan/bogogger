from django.db import models
from django.core.urlresolvers import reverse

from players.models import Player


class Game(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    min_players = models.PositiveIntegerField()
    max_players = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('game_detail', args=(), kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name


class GamePlay(models.Model):
    game = models.ForeignKey(Game)
    players = models.ManyToManyField(Player, through='PlayerRank')
    played_at = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('game_play_detail', args=(), kwargs={'pk': self.pk})


class PlayerRank(models.Model):
    player = models.ForeignKey(Player)
    game_play = models.ForeignKey(GamePlay)

    rank = models.PositiveIntegerField(null=True, blank=True)
