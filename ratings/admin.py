from django.contrib import admin

from .models import Rating, GamePlayerRating


admin.site.register(Rating)
admin.site.register(GamePlayerRating)
