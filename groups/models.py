from django.db import models
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField

from players.models import Player
from games.models import Game


class PlayerGroup(models.Model):

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    players = models.ManyToManyField(Player)
    games = models.ManyToManyField(Game)

    def get_absolute_url(self):
        return reverse('player_group_detail', args=(), kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.name
