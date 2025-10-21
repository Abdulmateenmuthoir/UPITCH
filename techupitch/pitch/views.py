from django.shortcuts import render

# Create your views here.


from .models import Match, Player, League, Team, Sport, Event

from django.utils import timezone

def index(request):
    """View function for home page of site."""

    num_matches = Match.objects.count()
    num_team = Team.objects.count()
    num_players = Player.objects.count()

    # Live Matches (limit 3)
    live_matches = Match.objects.filter(status__iexact='live').order_by('-start_time')[:3]
    num_live_matches = live_matches.count()

    # Upcoming Matches (start_time in future or status='upcoming')
    upcoming_matches = Match.objects.filter(
        start_time__gt=timezone.now()
    ).order_by('start_time')[:3]

    context = {
        'num_matches': num_matches,
        'num_team': num_team,
        'num_players': num_players,
        'num_live_matches': num_live_matches,
        'live_matches': live_matches,
        'upcoming_matches': upcoming_matches,  # ✅ added
    }

    return render(request, 'index.html', context)



from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F, Sum
from .models import League, Match  

def calculate_league_table(league):
    teams = league.teams.all()
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





class MatchDetailView(generic.DetailView):
    model = Match

    def get_object(self, queryset=None):
        match = super().get_object(queryset)
        match.auto_update_status()  # ✅ Automatically update the match status
        return match

from .models import Match






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




#############--UPDATE, DELETE, CREATE VIEW-----#######

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Player, Match, Team
from .forms import MatchForm, TeamForm
from django.contrib import messages


class PlayerCreate(PermissionRequiredMixin, CreateView):
    model = Player
    fields = [
        'name',
        'dept',
        'team',
        'date_of_birth',
        'position',
        'height_cm',
        'image',
        'university',
        'jersey_number',
    ]
    initial = {'jersey_number': 0}
    permission_required = 'catalog.add_player'  # replace `catalog` with your actual app name


class PlayerUpdate(PermissionRequiredMixin, UpdateView):
    model = Player
    fields = [
        'name',
        'dept',
        'team',
        'date_of_birth',
        'position',
        'height_cm',
        'image',
        'university',
        'jersey_number',
    ]
    permission_required = 'catalog.change_player'  # replace `catalog` with your app name



from django.shortcuts import render, get_object_or_404
from .models import Match

def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    return render(request, 'pitch/match_detail.html', {'match': match})

class PlayerDelete(PermissionRequiredMixin, DeleteView):
    model = Player
    success_url = reverse_lazy('players')  # name of your player list view URL
    permission_required = 'catalog.delete_player'  # replace `catalog` with your app name

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("player-delete", kwargs={"pk": self.object.pk})
            )


# --- MATCH CREATE VIEW ---
class MatchCreate(PermissionRequiredMixin, CreateView):
    model = Match
    form_class = MatchForm

    permission_required = 'catalog.add_match'
    template_name = 'catalog/match_form.html'
    success_url = reverse_lazy('matchs')  # ✅ Add this line

    def get_initial(self):
        return {'status': 'scheduled'}

    def form_valid(self, form):
        response = super().form_valid(form)
        match = self.object
        messages.success(
            self.request,
            f"✅ {match.home_team} vs {match.away_team} has been added successfully!"
        )
        return response


        

    def form_invalid(self, form):
        print("❌ Match form invalid:", form.errors)
        return super().form_invalid(form)

# --- MATCH UPDATE VIEW ---
class MatchUpdate(PermissionRequiredMixin, UpdateView):
    model = Match
    form_class = MatchForm

    permission_required = 'catalog.change_match'
    template_name = 'catalog/match_form.html'


# --- MATCH DELETE VIEW ---
class MatchDelete(PermissionRequiredMixin, DeleteView):
    model = Match
    success_url = reverse_lazy('matchs')
    permission_required = 'catalog.delete_match'
    template_name = 'catalog/match_confirm_delete.html'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse_lazy("match-delete", kwargs={"pk": self.object.pk})
            )


#-------Team Create View----------#

class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'catalog/team_form.html'

    def form_valid(self, form):
        # Example: set sport automatically based on the league
        league_id = self.request.POST.get('league')
        league = League.objects.get(id=league_id)
        form.instance.sport = league.sport  # or whatever logic fits

        return super().form_valid(form)


class TeamUpdate(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'catalog/team_form.html'
    success_url = reverse_lazy('teams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sports'] = Sport.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, f"{form.instance.name} has been updated successfully.")
        return super().form_valid(form)


class TeamDelete(DeleteView):
    model = Team
    template_name = 'catalog/team_confirm_delete.html'
    success_url = reverse_lazy('teams')

    def delete(self, request, *args, **kwargs):
        team = self.get_object()
        messages.success(request, f"{team.name} has been deleted successfully.")
        return super().delete(request, *args, **kwargs)





from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

def postpone_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.user.is_staff:
        match.postpone()
        messages.warning(request, "Match has been postponed.")
    return redirect('match-detail', pk=pk)

def resume_match(request, pk):
    match = get_object_or_404(Match, pk=pk)
    if request.user.is_staff:
        new_time = timezone.now() + timezone.timedelta(days=1)  # example: resume tomorrow
        match.resume(new_start_time=new_time)
        messages.success(request, f"Match resumed and rescheduled for {new_time:%b %d, %Y %H:%M}.")
    return redirect('match-detail', pk=pk)




from django.shortcuts import render
from .models import Match

def match_list(request):
    # Fetch all matches, grouped by league
    matches = Match.objects.select_related('league').order_by('league__name', 'start_time')

    # 🔁 Automatically update status before displaying
    for match in matches:
        match.auto_update_status()

    # Group matches under each league name
    grouped_matches = {}
    for match in matches:
        league_name = match.league.name if match.league else "Uncategorized"
        grouped_matches.setdefault(league_name, []).append(match)

    return render(request, 'pitch/match_list.html', {
        'grouped_matches': grouped_matches,
    })


from django.http import JsonResponse
from django.utils import timezone
from .models import Match

def live_upcoming_matches(request):
    """Return live and upcoming matches as JSON for AJAX updates."""
    now = timezone.now()

    # Auto-update statuses if you have this method
    for match in Match.objects.exclude(status='postponed'):
        match.auto_update_status()

    live_matches = Match.objects.filter(status='live').select_related('league', 'home_team', 'away_team')
    upcoming_matches = Match.objects.filter(start_time__gt=now).select_related('league', 'home_team', 'away_team')

    data = {
        'live_matches': [
            {
                'league': m.league.name,
                'home_team': m.home_team.name,
                'away_team': m.away_team.name,
                'home_score': m.home_score or 0,
                'away_score': m.away_score or 0,
                'status': m.status,
                'start_time': m.start_time.strftime('%H:%M'),
            }
            for m in live_matches
        ],
        'upcoming_matches': [
            {
                'league': m.league.name,
                'home_team': m.home_team.name,
                'away_team': m.away_team.name,
                'start_time': m.start_time.strftime('%H:%M'),
            }
            for m in upcoming_matches
        ]
    }

    return JsonResponse(data)
