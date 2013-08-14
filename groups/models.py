from django.db import models
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField


class PlayerGroup(models.Model):

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    players = models.ManyToManyField('players.Player')
    games = models.ManyToManyField('games.Game')

    def get_absolute_url(self):
        return reverse('player_group_detail', args=(), kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name


class GroupRating(models.Model):

    group = models.ForeignKey(PlayerGroup)
    player = models.ForeignKey('players.Player')
    game_play = models.ForeignKey('games.GamePlay')
    rating = models.PositiveIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.group, self.player, self.game_play.game, self.rating)

    def save(self, *args, **kwargs):
        group_rating = super(GroupRating, self).save(*args, **kwargs)

        try:
            ordered_group_ratings = GroupRating.objects.filter(
                player=self.player,
                game_play__game=self.game_play.game,
                group=self.group,
            ).order_by(
                '-game_play__played_at',
                '-pk',
            )
            group_game_rating = GroupGamePlayerRating.objects.get(
                player=self.player,
                game=self.game_play.game,
                group=self.group,
            )
            group_game_rating.rating = self
            group_game_rating.save()
        except GroupGamePlayerRating.DoesNotExist:
            GroupGamePlayerRating.objects.create(
                player=self.player,
                game=self.game_play.game,
                group=self.group,
                rating=self,
            )


class GroupGamePlayerRating(models.Model):

    player = models.ForeignKey('players.Player')
    game = models.ForeignKey('games.Game')
    rating = models.ForeignKey(GroupRating)
    group = models.ForeignKey(PlayerGroup)

    class Meta:
        unique_together = ('player', 'game', 'group',)

    def __unicode__(self):
        return u'%s' % self.rating


class Invite(models.Model):

    email = models.EmailField()
    group = models.ForeignKey(PlayerGroup)
    hash = models.CharField(max_length=255)

    class Meta:
        unique_together = ('email', 'group',)

    def __unicode__(self):
        return u'%s - %s' % (self.email, self.group,)
