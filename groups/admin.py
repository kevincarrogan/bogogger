from django.contrib import admin

from .models import PlayerGroup, GroupRating, GroupGamePlayerRating


admin.site.register(PlayerGroup)
admin.site.register(GroupRating)
admin.site.register(GroupGamePlayerRating)
