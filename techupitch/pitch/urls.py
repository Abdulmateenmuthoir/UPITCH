from django.urls import path
from . import views

urlpatterns = [

]
urlpatterns = [
    path('', views.index, name='index'),
    path('league/<int:league_id>/table/', views.league_table_view, name='league-table'),
    path('matchs/', views.MatchListView.as_view(), name='matchs'),

    path('match/<int:pk>', views.MatchDetailView.as_view(), name='match-detail'),

    path('leagues/', views.LeagueListView.as_view(), name='leagues'),
    path('league/<int:pk>/table/', views.league_table_view, name='league-detail'),

    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('teams/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
    path('players/', views.PlayerListView.as_view(), name= 'players'),
    path('players/<int:pk>', views.PlayerDetailView.as_view(), name= 'player-detail'),
    path('sports/', views.SportListView.as_view(), name= 'sports' ),

    # Add Django site authentication urls (for login, logout, password management)

    urlpatterns += [
        path('accounts/', include('django.contrib.auth.urls')),
    ]


]
