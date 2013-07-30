import math

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from games.models import GamePlay, Game
from players.models import Player


class Rating(models.Model):

    player = models.ForeignKey(Player)
    game_play = models.ForeignKey(GamePlay)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.player, self.game_play.game, self.rating)

    def save(self, *args, **kwargs):
        rating = super(Rating, self).save(*args, **kwargs)

        try:
            ordered_ratings = Rating.objects.filter(
                player=self.player,
                game_play__game=self.game_play.game,
            ).order_by(
                '-game_play__played_at',
                '-pk',
            )
            rating = ordered_ratings[0]
            game_rating = GamePlayerRating.objects.get(
                player=self.player,
                game=self.game_play.game,
            )
            game_rating.rating = self
            game_rating.save()
        except GamePlayerRating.DoesNotExist:
            GamePlayerRating.objects.create(
                player=self.player,
                game=self.game_play.game,
                rating=self,
            )

    @staticmethod
    def get_win_probability(player_rating, oppenent_rating):
        return 1 / (10 ** ((oppenent_rating - player_rating) / 400.0) + 1)

    @staticmethod
    def get_adjustment(score, probability):
        return settings.ELO_K_VALUE * (score - probability)


class GamePlayerRating(models.Model):

    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    rating = models.ForeignKey(Rating)

    class Meta:
        unique_together = ('player', 'game',)

    def __unicode__(self):
        return u'%s' % self.rating
