from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('league/<int:league_id>/table/', views.league_table_view, name='league-table'),


    path('matchs/', views.match_list, name='matchs'),
    path('match/<int:pk>', views.MatchDetailView.as_view(), name='match-detail'),

    path('leagues/', views.LeagueListView.as_view(), name='leagues'),
    path('league/<int:pk>/table/', views.league_table_view, name='league-detail'),

    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('teams/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),

    path('players/', views.PlayerListView.as_view(), name='players'),
    path('players/<int:pk>', views.PlayerDetailView.as_view(), name='player-detail'),

    path('sports/', views.SportListView.as_view(), name='sports'),

    # Django authentication (login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
]


urlpatterns += [
    path('player/create/', views.PlayerCreate.as_view(), name='player-create'),
    path('player/<int:pk>/update/', views.PlayerUpdate.as_view(), name='player-update'),
    path('player/<int:pk>/delete/', views.PlayerDelete.as_view(), name='player-delete'),

]

# ✅ Match CRUD
urlpatterns += [
    path('ajax/matches/', views.live_upcoming_matches, name='ajax-matches'),
    path('match/create/', views.MatchCreate.as_view(), name='match-create'),
    path('match/<int:pk>/postpone/', views.postpone_match, name='postpone-match'),
    path('match/<int:pk>/resume/', views.resume_match, name='resume-match'),
    path('match/<int:pk>/update/', views.MatchUpdate.as_view(), name='match-update'),
    path('match/<int:pk>/delete/', views.MatchDelete.as_view(), name='match-delete'),
]


#------TEAM CRUD------#

urlpatterns += [
    path('team/create/', views.TeamCreate.as_view(), name='team-create'),
    path('team/<int:pk>/update/', views.TeamUpdate.as_view(), name='team-update'),
    path('team/<int:pk>/delete/', views.TeamDelete.as_view(), name='team-delete'),
]
