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
