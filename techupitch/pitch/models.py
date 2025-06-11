from django.db import models

# Create your models here.
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.shortcuts import render

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

class League(models.Model):
    name = models.CharField(max_length=200)
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE)
    university = models.CharField(max_length=100, blank=True, null=True) # Optional, country of the league.
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
    league = models.ForeignKey(League, on_delete=models.CASCADE, default=1)  # or other on_delete options

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular team."""
        return reverse('team-detail', args=[str(self.id)])

class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.RESTRICT)
    home_team = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name="home_matches")
    away_team = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name="away_matches")
    start_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('live', 'Live'), ('finished', 'Finished')])
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.home_team} vs {self.away_team}'

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this match."""
        return reverse('match-detail', args=[str(self.id)])


from django.db import models





class Player(models.Model):
    """Model representing an player."""
    dept = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='player_images/', blank=True, null=True)
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
    table_data = calculate_league_table(league, season)
    return render(request, 'league_table.html', {'table': table_data, 'league': league})