from django import forms
from django.forms.models import BaseInlineFormSet

from ratings.models import Rating
from groups.models import GroupRating

from .models import GamePlay, PlayerRank


class GamePlayForm(forms.ModelForm):

    class Meta:
        model = GamePlay
        fields = ('game', 'played_at',)

    def __init__(self, *args, **kwargs):
        player = kwargs.pop('player')

        super(GamePlayForm, self).__init__(*args, **kwargs)

        queryset = self.fields['game'].queryset
        queryset = queryset.filter(playergroup__players=player)
        self.fields['game'].queryset = queryset


class GamePlayFromGameForm(forms.ModelForm):
    played_at = forms.SplitDateTimeField()

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

        covered_groups = []

        # Run this first so that changing the players
        # overall rating doesn't affect their group rating
        for rank in ranks:
            player = rank.player

            for group in player.playergroup_set.all():
                if group not in covered_groups:
                    # Get the other ranks of players that are in this group.
                    # May be none.
                    ranks_for_group = self.get_players_in_group_by_ranks(group, ranks)

                    # Get the new ratings for this particular group
                    for ratings_player, new_rating in self.get_new_ratings_for_group(game_play.game, group, ranks_for_group):
                        GroupRating.objects.create(
                            player=ratings_player,
                            game_play=game_play,
                            rating=new_rating,
                            group=group,
                        )
                    covered_groups.append(group)

        for player, new_rating in self.get_new_ratings(game_play.game, ranks):
            Rating.objects.create(
                player=player,
                game_play=game_play,
                rating=new_rating,
            )

        return ranks

    def get_players_in_group_by_ranks(self, group, ranks):
        ranks = ranks.filter(player__playergroup=group)

        return ranks

    def get_new_ratings_for_group(self, game, group, ranks):
        new_ratings = []
        for rank in ranks:
            player_rating = self.get_player_group_game_rating(game, group, rank)

            opponent_ranks = ranks.exclude(player=rank.player)
            opponent_ratings = [
                self.get_player_group_game_rating(game, group, opponent_rank)
                for opponent_rank in opponent_ranks
            ]
            new_ratings.append(
                (rank.player, player_rating[1] + sum(Rating.get_adjustments(player_rating, opponent_ratings)))
            )

        return new_ratings

    def get_player_group_game_rating(self, game, group, rank):
        return (rank.rank, rank.player.get_current_group_rating_for_game(game, group),)

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
