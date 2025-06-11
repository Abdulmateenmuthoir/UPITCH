from django.shortcuts import render

# Create your views here.


from .models import Match, Player, League, Team, Sport, Event

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_matches = Match.objects.all().count()
    num_team = Team.objects.all().count()

    # Available live matches(status = 'a')
    num_live_matches = Match.objects.filter(status__exact='Live').count()
    live_matches = Match.objects.filter(status__exact='live')  # Or status__iexact
    print(live_matches.query)  # Print the SQL query being executed
    num_live_matches = live_matches.count()
    print(f"Number of live matches found: {num_live_matches}")

    # The 'all()' is implied by default.
    num_players = Player.objects.count()

    context = {
        'num_matches': num_matches,
        'num_team': num_team,
        'num_live_matches': num_live_matches,
        'num_players': num_players,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F, Sum
from .models import League, Match  

def calculate_league_table(league):
    teams = league.team_set.all()
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

    table = sorted(table, key=lambda x: (x['points'], x['goal_difference'], x['goals_for']), reverse=True)

    for index, row in enumerate(table):
        row['position'] = index + 1

    return table


def league_table_view(request, league_id):
    league = get_object_or_404(League, pk=league_id)
    table_data = calculate_league_table(league)
    return render(request, 'league_table.html', {'table': table_data, 'league': league})





from django.views import generic

class MatchListView(generic.ListView):
    model = Match   


class MatchDetailView(generic.DetailView):
    model = Match

class LeagueListView(generic.ListView):
    model = League


class TeamListView(generic.ListView):
    model = Team


class TeamDetailView(generic.DetailView):
    model = Team

class PlayerListView(generic.ListView):
    model = Player


class PlayerDetailView(generic.DetailView):
    model = Player

class SportListView(generic.ListView):
    model = Sport


