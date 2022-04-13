from django.urls import path

from SofiaFooty.web.views import show_home, show_public
from SofiaFooty.web.views_p.match_views import EditMatchView, EditMatchDetailsView
from SofiaFooty.web.views_p.profile_views import UserLoginView, UserLogoutView, delete_profile, UserRegisterView, \
    ProfileDetailsView, ProfileEditView
from SofiaFooty.web.views_p.team_views import  JoinTeamSearchResultsView, JoinTeamView, leave_team, \
    CreateTeamView, TeamDetailsView, SearchTeams
from SofiaFooty.web.views_p.tournament_views import CreateTournamentView, TournamentDetailsView,  \
    JoinTournamentSearchResultsView, JoinTournamentView, leave_tournament, TournamentPublicDetailsView, \
    ManageTournamentView, AllTournamentsView, TournamentPublicSearchResultsView, SearchTournaments

urlpatterns = (
    # path('', UserLoginView.as_view(), name='show start'),- beshe predi taka

    path('', show_public, name='show public'),  # tova e novo, public part
    path('public/tournament/details/<int:pk>/', TournamentPublicDetailsView.as_view(), name='show public tournament details'),# tova e novo, public part


    path('login/', UserLoginView.as_view(), name='show start'),
    path('register/', UserRegisterView.as_view(), name='create profile'),
    path('logout/', UserLogoutView.as_view(), name='show logout'),

    path('home/', show_home, name='show home'),

    path('profile/details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/delete/', delete_profile, name='profile delete'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile edit'),

    path('team/create/', CreateTeamView.as_view(), name='create team'),
    path('team/details/<int:pk>/', TeamDetailsView.as_view(), name='team details'),
    path('team/search/', SearchTeams.as_view(), name='join team'),
    path('team/search/results/', JoinTeamSearchResultsView.as_view(), name='search team result'),
    path('team/join/confirm/<int:pk>/', JoinTeamView.as_view(), name='join team confirm'),
    path('team/leave/confirm/<int:pk>/', leave_team, name='leave team confirm'),

    path('tournament/create/', CreateTournamentView.as_view(), name='create tournament'),
    path('tournament/details/<int:pk>/', TournamentDetailsView.as_view(), name='tournament details'),

    path('tournament/join/', SearchTournaments.as_view(), name='search tournaments'),
    path('tournament/join/search/', JoinTournamentSearchResultsView.as_view(), name='search tournaments results'),
    path('tournament/join/confirm/<int:pk>/', JoinTournamentView.as_view(), name='join tournament confirm'),
    path('tournament/leave/confirm/<int:pk>/', leave_tournament, name='leave tournament confirm'),
    path('tournament/manage/', ManageTournamentView.as_view(), name='manage tournament'),
    path('tournament/tournaments-all/', AllTournamentsView.as_view(), name = 'all tournaments'),
    path('tournaments/tournaments-all/search-result/', TournamentPublicSearchResultsView.as_view(), name = 'search tournament public results'),


    path('tournament/match/edit/<int:pk>/', EditMatchView.as_view(), name = 'edit match'),
    path('tournament/match/edit/details/<int:pk>/', EditMatchDetailsView.as_view(), name = 'edit match details'),

)
