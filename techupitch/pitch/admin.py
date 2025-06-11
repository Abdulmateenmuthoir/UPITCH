from django.contrib import admin

# Register your models here.
from .models import Sport, League, Team, Match, Player, Event

admin.site.register(Sport)
admin.site.register(League)
#admin.site.register(Team)
#admin.site.register(Match)
#admin.site.register(Player)
#admin.site.register(Event)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'dept', 'team', 'date_of_birth')

    fields = ['name', 'dept', ('team', 'date_of_birth')]

admin.site.register(Player, PlayerAdmin)


class MatchAdmin(admin.ModelAdmin):

    list_display = ('home_team', 'away_team' , 'start_time', 'status')

admin.site.register(Match, MatchAdmin)


class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', 'logo')

admin.site.register(Team, TeamAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('match', 'event_type', 'player_name')
    
admin.site.register(Event, EventAdmin)