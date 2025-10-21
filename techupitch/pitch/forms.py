from django import forms
from .models import Match, Team

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['league', 'home_team', 'away_team', 'start_time', 'home_score', 'away_score']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'logo', 'league','university']

