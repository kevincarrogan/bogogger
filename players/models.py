from django.db import models
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from autoslug import AutoSlugField


class Player(models.Model):
    user = models.ForeignKey(get_user_model(), blank=True, null=True)
    slug = AutoSlugField(
        populate_from='fullname',
        unique=True,
    )

    # Fields if this isn't tied to a user
    _first_name = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='First name',
    )
    _last_name = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='Last name',
    )

    @property
    def fullname(self):
        if self.first_name and self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        else:
            return self.user.username

    def get_absolute_url(self):
        return reverse('player_detail', args=(), kwargs={'slug': self.slug})

    def get_from_self_or_user(self, field_name):
        if self.user:
            inst = self.user
        else:
            inst = self
            field_name = '_%s' % field_name

        return getattr(inst, field_name)

    @property
    def first_name(self):
        return self.get_from_self_or_user('first_name')

    @property
    def last_name(self):
        return self.get_from_self_or_user('last_name')

    def __unicode__(self):
        if self.first_name:
            return u'%s %s' % (self.first_name, self.last_name)
        else:
            return self.slug

    def get_current_rating_for_game(self, game):
        try:
            ratings = self.rating_set.filter(game_play__game=game)
            ratings = ratings.order_by('-game_play__played_at', '-pk')

            return ratings[0].rating
        except IndexError:
            return settings.INITIAL_ELO_RATING

    def get_current_group_rating_for_game(self, game, group):
        try:
            group_ratings = self.grouprating_set.filter(group=group, game_play__game=game)
            group_ratings = group_ratings.order_by('-game_play__played_at', '-pk')

            return group_ratings[0].rating
        except IndexError:
            return self.get_current_rating_for_game(game)


@receiver(post_save, sender=get_user_model())
def create_player_from_user(sender, **kwargs):
    user = kwargs['instance']

    Player.objects.create(
        user=user,
    )
