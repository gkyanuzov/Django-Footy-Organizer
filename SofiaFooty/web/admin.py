from cProfile import Profile

from django.contrib import admin

# Register your models here.
from SofiaFooty.web.models import Team, Tournament, Match, Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.created_by != request.user:
            return False
        return True

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_players')


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    pass

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass

