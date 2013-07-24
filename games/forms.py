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

        if game_play.game.min_players == 2 and game_play.game.max_players == 2:
            # For now we only support ELO for two player games
            ordered_ranks = game_play.playerrank_set.order_by('rank')
            draw = True
            current_rank = ordered_ranks[0].rank
            for rank in ordered_ranks[1:]:
                draw = current_rank == rank.rank
                if not draw:
                    break

            ordered_ratings = [rank.player.get_current_rating_for_game(game_play.game) for rank in ordered_ranks]

            new_ratings = Rating.get_new_ratings(ordered_ratings[0], ordered_ratings[1], draw)

            for rank, new_rating in zip(ordered_ranks, new_ratings):
                Rating.objects.create(
                    player=rank.player,
                    game_play=rank.game_play,
                    rating=new_rating,
                )

        return ranks
