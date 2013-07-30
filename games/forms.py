from django import forms
from django.forms.models import BaseInlineFormSet
from django.conf import settings

from ratings.models import Rating

from .models import GamePlay, PlayerRank


class GamePlayForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('game', 'played_at',)


class GamePlayFromGameForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('played_at',)


class GamePlayFromCoopGameForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('played_at', 'win',)


class PlayerRankForm(forms.ModelForm):

    class Meta:
        model = PlayerRank


class PlayerRankCoopGameForm(forms.ModelForm):

    class Meta:
        model = PlayerRank
        fields = ('player',)


class PlayerRankFormset(BaseInlineFormSet):

    def clean(self, *args, **kwargs):
        game = self.instance.game
        min_players = game.min_players

        if len(self.forms) < min_players:
            raise forms.ValidationError('This game requires at least %d players to have played' % min_players)

        return super(PlayerRankFormset, self).clean(*args, **kwargs)

    def save(self):
        ranks = super(PlayerRankFormset, self).save()

        game_play = self.instance

        ranks = game_play.playerrank_set.all()

        for player, new_rating in self.get_new_ratings(game_play.game, ranks):
            Rating.objects.create(
                player=player,
                game_play=game_play,
                rating=new_rating,
            )

        return ranks

    def get_player_game_rating(self, game, rank):
        return (rank.rank, rank.player.get_current_rating_for_game(game),)

    def get_new_ratings(self, game, ranks):
        new_ratings = []
        for rank in ranks:
            player_rating = self.get_player_game_rating(game, rank)

            opponent_ranks = ranks.exclude(player=rank.player)
            opponent_ratings = [
                self.get_player_game_rating(game, opponent_rank)
                for opponent_rank in opponent_ranks
            ]
            new_ratings.append(
                (rank.player, player_rating[1] + sum(Rating.get_adjustments(player_rating, opponent_ratings)))
            )

        return new_ratings
