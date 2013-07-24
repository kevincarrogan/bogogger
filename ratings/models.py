import math

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from games.models import GamePlay
from players.models import Player


def get_win_probability(current_player_rating, oppenent_rating):
    return 1 / (10 ** ((oppenent_rating - current_player_rating) / 400.0) + 1)


def get_new_rating(rating, score, probability):
    return rating + (settings.ELO_K_VALUE * (score - probability))


class Rating(models.Model):

    player = models.ForeignKey(Player)
    game_play = models.ForeignKey(GamePlay)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s - %s' % (self.player, self.game_play.game, self.rating)

    @staticmethod
    def get_new_ratings(winner_rating, loser_rating, draw=False):
        winner_probability = get_win_probability(winner_rating, loser_rating)
        loser_probability = get_win_probability(loser_rating, winner_rating)

        if not draw:
            winner_rating = get_new_rating(winner_rating, settings.ELO_WIN_SCORE, winner_probability)
            loser_rating = get_new_rating(loser_rating, settings.ELO_LOSE_SCORE, loser_probability)
        else:
            winner_rating = get_new_rating(winner_rating, settings.ELO_DRAW_SCORE, winner_probability)
            loser_rating = get_new_rating(loser_rating, settings.ELO_DRAW_SCORE, loser_probability)

        return (winner_rating, loser_rating,)
