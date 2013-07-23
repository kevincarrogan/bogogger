from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from games.models import GamePlay
from players.models import Player


class Rating(models.Model):

    player = models.ForeignKey(Player)
    game_play = models.ForeignKey(GamePlay)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s - %s' % (self.player, self.game_play.game, self.rating)
