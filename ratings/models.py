from django.db import models
from django.conf import settings


class Rating(models.Model):

    player = models.ForeignKey('players.Player')
    game_play = models.ForeignKey('games.GamePlay')
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

    @staticmethod
    def get_adjustments(player_rating, opponent_ratings):
        adjustments = []

        player_rank, player_rating = player_rating

        for opponent_rank, opponent_rating in opponent_ratings:
            win_probability = Rating.get_win_probability(player_rating, opponent_rating)
            if player_rank < opponent_rank:
                score = settings.ELO_WIN_SCORE
            elif player_rank > opponent_rank:
                score = settings.ELO_LOSE_SCORE
            else:
                score = settings.ELO_DRAW_SCORE
            adjustments.append(Rating.get_adjustment(score, win_probability))

        return adjustments


class GamePlayerRating(models.Model):

    player = models.ForeignKey('players.Player')
    game = models.ForeignKey('games.Game')
    rating = models.ForeignKey(Rating)

    class Meta:
        unique_together = ('player', 'game',)

    def __unicode__(self):
        return u'%s' % self.rating
