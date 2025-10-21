from django.db import models
import uuid

# Create your models here.
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.shortcuts import render

from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.utils import timezone


from datetime import timedelta

from django.db.models import Q, Sum, Count, F



class Sport(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a Sport (e.g. Football, TabbleTennis or Basket Ball etc.)"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular sport instance."""
        return reverse('sport-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='sport_name_case_insensitive_unique',
                violation_error_message = "sport already exists (case insensitive match)"
            ),
        ]





class University(models.Model):
    name = models.CharField(max_length=160, unique=True)
    short_name = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    logo = models.ImageField(upload_to="universities/logos/", blank=True)

    # Optional: add social handles or website
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=60, blank=True)
    twitter = models.CharField(max_length=60, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.short_name or self.name




class League(models.Model):
    
    name = models.CharField(max_length=200)
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE)
    
    university = models.ForeignKey(
        University, null=True, blank=True, on_delete=models.SET_NULL, related_name="league"
    )
    
    logo = models.ImageField(upload_to='league_logos/', blank=True, null=True) # Optional, league logo.
    abbreviation = models.CharField(max_length=10, blank=True, null=True) # Optional, short name or abbreviation.

    def __str__(self):
        return self.name

    def get_absolute_url(self):

        
        """Returns the url to access a particular sport."""
        return reverse('league-detail', args=[str(self.id)])

class Team(models.Model):
    name = models.CharField(max_length=200)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    league = models.ManyToManyField(League, related_name="teams", blank=True)

    
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    def league_names(self):
        return ",".join(self.league.values_list("name", flat=True))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular team."""
        return reverse('team-detail', args=[str(self.id)])

from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class Match(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('finished', 'Finished'),
        ('postponed', 'Postponed'),
    ]

    league = models.ForeignKey('League', on_delete=models.RESTRICT)
    home_team = models.ForeignKey('Team', on_delete=models.RESTRICT, related_name="home_matches")
    away_team = models.ForeignKey('Team', on_delete=models.RESTRICT, related_name="away_matches")
    start_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', editable=False)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.home_team} vs {self.away_team}'

    def get_absolute_url(self):
        return reverse('match-detail', args=[str(self.id)])

    # ✅ Manually postpone a match
    def postpone(self):
        """Pause this match — no timer updates while postponed."""
        self.status = 'postponed'
        self.save(update_fields=['status'])

    # ✅ Resume a postponed match
    def resume(self, new_start_time=None):
        """Resume a postponed match, optionally rescheduling."""
        if new_start_time:
            self.start_time = new_start_time
        self.status = 'scheduled'
        self.save(update_fields=['status', 'start_time'])

    # ✅ Automatically determine current status
    def auto_update_status(self):
        """Automatically update match status based on time."""
        if self.status == 'postponed':
            return  # Skip postponed matches

        now = timezone.now()
        match_duration = timedelta(minutes=90)

        # Decide new status
        if now < self.start_time:
            new_status = 'scheduled'
        elif self.start_time <= now < self.start_time + match_duration:
            new_status = 'live'
        else:
            new_status = 'finished'

        # Update if changed
        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])



from django.db import models





class Player(models.Model):
    """Model representing an player."""
    dept = models.CharField(max_length=100)

    name = models.CharField(max_length=200)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    date_of_birth = models.DateField(null=True, blank=True)

    position = models.CharField(max_length=50, choices=[ ("GK", "Goalkeeper"), ("DF", "Defender"), ("MF", "Midfielder"), ("FW", "Forward"),], null=True )

    height_cm = models.PositiveIntegerField(blank=True, null=True)

    image = models.ImageField(upload_to='player_images/', blank=True, null=True)

    university = models.ForeignKey(
        University, null=True, blank=True, on_delete=models.SET_NULL, related_name="players"
    )

    jersey_number = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    
    class Meta:
        ordering = ['name', 'team'] 

    def get_absolute_url(self):
        """Returns the URL to access a particular player instance."""
        return reverse('player-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}, {self.team}'


    


class Event(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=500) # use choices here.
    event_time = models.DateTimeField()
    player_name = models.ForeignKey(Player , on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.event_type}'

    def get_absolute_url(self):
        """Returns the url to access a particular team."""
        return reverse('event-detail', args=[str(self.id)])



from django.db.models import Q, Sum, Count

def calculate_league_table(league):
    teams = league.team_set.all()  # Get all teams in the league
    table = []

    for team in teams:
        matches = Match.objects.filter(
            Q(league=league) & (Q(home_team=team) | Q(away_team=team))
        )
        

        played = matches.count()
        wins = matches.filter(
            (Q(home_team=team) & Q(home_score__gt=F('away_score'))) |
            (Q(away_team=team) & Q(away_score__gt=F('home_score')))
        ).count()
        draws = matches.filter(Q(home_score=F('away_score'))).count()
        losses = played - wins - draws

        goals_for = matches.filter(home_team=team).aggregate(Sum('home_score'))['home_score__sum'] or 0
        goals_for += matches.filter(away_team=team).aggregate(Sum('away_score'))['away_score__sum'] or 0

        goals_against = matches.filter(home_team=team).aggregate(Sum('away_score'))['away_score__sum'] or 0
        goals_against += matches.filter(away_team=team).aggregate(Sum('home_score'))['home_score__sum'] or 0

        goal_difference = goals_for - goals_against
        points = (wins * 3) + draws

        table.append({
            'team': team,
            'played': played,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goal_difference,
            'points': points,
        })

    # Sort the table by points, goal difference, etc.
    table = sorted(table, key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)

    # Add position
    for index, row in enumerate(table):
        row['position'] = index + 1

    return table


def league_table_view(request, league_id, season_id=None):
    league = League.objects.get(pk=league_id)
    table_data = calculate_league_table(league)
    return render(request, 'league_table.html', {'table': table_data, 'league': league})