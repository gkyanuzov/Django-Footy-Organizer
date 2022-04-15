import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin

from SofiaFooty.web.decorators import captaincy_required, no_tournament_required, tournament_creator_required, \
    tournament_required, matching_team_required
from SofiaFooty.web.forms import TournamentCreationForm, JoinTournamentForm, LeaveTournamentForm, MatchCreationForm, \
    EditMatchForm, EditTournamentForm, RemoveTeamForm, LeaveTournamentCreatorForm
from SofiaFooty.web.models import Tournament, Player, Team, SofiaFootyUser, Match

create_tournament_decorators = [login_required, captaincy_required, no_tournament_required, ]
manage_tournament_decorators = [login_required, captaincy_required, tournament_creator_required, ]
join_tournament_decorators = [login_required, captaincy_required, no_tournament_required, ]
leave_tournament_decorators = [login_required, captaincy_required, tournament_required, ]

edit_tournament_and_remove_teams_decorators = [login_required, captaincy_required, tournament_creator_required,]


@method_decorator(create_tournament_decorators, name='dispatch')
class CreateTournamentView(CreateView):
    form_class = TournamentCreationForm
    template_name = 'tournament/create_tournament.html'
    success_url = reverse_lazy('show home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        context['player'] = player
        return context


class TournamentDetailsView(DetailView, LoginRequiredMixin):
    model = Tournament
    template_name = 'tournament/tournament_details.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        player = Player.objects.get(pk=self.request.user.id)

        teams = Team.objects.filter(tournament_id=self.object.id)
        matches = Match.objects.filter(tournament_id=self.object.id)
        matches = sorted(list(matches), key=lambda m: m.date, reverse=True)

        is_full = len(teams) == int(self.object.size)

        teams_to_show = list(teams)
        try:
            teams_to_show = list(teams_to_show)[0:12]
        except IndexError:
            teams_to_show = teams_to_show

        creator = None
        if self.object.creator is not None:
            creator = self.object.creator.player

        is_active = self.object.is_active == True

        context['is_active'] = is_active
        context['is_full'] = is_full
        context['teams'] = teams
        context['teams_to_show'] = teams_to_show
        context['player'] = player
        context['is_creator'] = player.is_tournament_creator == True
        context['creator'] = creator
        context['matches'] = matches
        return context


class TournamentPublicDetailsView(DetailView):
    model = Tournament
    template_name = 'tournament/tournament_details_public.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teams = Team.objects.filter(tournament_id=self.object.id)

        teams_to_show = list(teams)

        try:
            teams_to_show = teams_to_show[0:12]
        except IndexError:
            teams_to_show = teams_to_show

        creator = None
        if self.object.creator is not None:
            creator = self.object.creator.player

        matches = Match.objects.filter(tournament_id=self.object.id)
        matches = sorted(list(matches), key=lambda m: m.date, reverse=True)

        context['teams'] = teams
        context['teams_to_show'] = teams_to_show
        context['creator'] = creator
        context['matches'] = matches
        return context


class AllTournamentsPublicView(ListView):
    model = Tournament
    template_name = 'tournament/all_tournaments.html'
    paginate_by = 12


class TournamentPublicSearchResultsView(ListView):
    model = Tournament
    template_name = "tournament/tournament_public_search_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Tournament.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


@method_decorator(manage_tournament_decorators, name='dispatch')
class ManageTournamentView(CreateView):
    model = Match
    form_class = MatchCreationForm
    template_name = 'tournament/manage_tournament.html'
    success_url = reverse_lazy('manage tournament')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_id = self.request.user.id
        player = Player.objects.get(pk=player_id)
        team = player.team
        tournament = team.tournament
        matches = Match.objects.filter(tournament_id=tournament.id)
        sorted_matches = sorted(list(matches), key=lambda m: m.date)
        first_round_size = int(tournament.size) / 2
        first_round_size = int(first_round_size)
        second_round_size = first_round_size / 2
        second_round_size = int(second_round_size)
        third_round_size = second_round_size / 2
        third_round_size = int(third_round_size)
        fourth_round_size = third_round_size / 2
        fourth_round_size = int(fourth_round_size)
        fifth_round_size = 1
        form_active = False
        try:
            if datetime.date.today() >= sorted_matches[-1].date:
                form_active = True
        except IndexError:
            pass
        try:
            first_round_matches = sorted_matches[0:first_round_size]
            second_round_matches = sorted_matches[first_round_size:first_round_size + second_round_size]
            third_round_matches = sorted_matches[
                                  first_round_size + second_round_size: first_round_size + second_round_size + third_round_size]
            fourth_round_matches = sorted_matches[
                                   first_round_size + second_round_size + third_round_size:first_round_size + second_round_size + third_round_size + fourth_round_size]
            fifth_round_matches = sorted_matches[
                                  first_round_size + second_round_size + third_round_size + fourth_round_size:first_round_size + second_round_size + third_round_size + fourth_round_size + fifth_round_size]
        except IndexError:
            first_round_matches = []
            second_round_matches = []
            third_round_matches = []
            fourth_round_matches = []
            fifth_round_matches = []

        context['form_active'] = form_active
        context['player'] = player
        context['tournament'] = tournament
        context['matches'] = matches
        context['first_round_size'] = first_round_size
        context['second_round_size'] = second_round_size
        context['third_round_size'] = third_round_size
        context['fourth_round_size'] = fourth_round_size
        context['first_round_matches'] = first_round_matches
        context['second_round_matches'] = second_round_matches
        context['third_round_matches'] = third_round_matches
        context['fourth_round_matches'] = fourth_round_matches
        context['fifth_round_matches'] = fifth_round_matches
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['player'] = Player.objects.get(pk=self.request.user.id)
        kwargs['tournament'] = Tournament.objects.get(pk=kwargs['player'].team.tournament.id)

        return kwargs


# @login_required(redirect_field_name='show start')
# def search_tournament(request):
#     tournaments = Tournament.objects.all()
#     player = Player.objects.get(pk=request.user.id)
#     context = {
#         'tournaments': tournaments,
#         'player': player,
#     }
#     return render(request, 'tournament/search_tournament.html', context)

@method_decorator(edit_tournament_and_remove_teams_decorators, name='dispatch')
class EditTournamentView(UpdateView):
    model = Tournament
    template_name = 'tournament/edit_tournament.html'
    form_class = EditTournamentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        teams = Team.objects.filter(tournament_id=self.object.id)
        context['player'] = player
        context['teams'] = teams
        return context

    def get_success_url(self):
        return reverse_lazy('tournament details', kwargs={'pk': self.object.id})


# @method_decorator(edit_team_and_remove_players_decorators, name='dispatch')
class RemoveTeamView(UpdateView):
    model = Team
    template_name = 'tournament/remove_teams.html'
    form_class = RemoveTeamForm
    context_object_name = 'team_to_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        context['player'] = player
        return context

    def get_success_url(self):
        return reverse_lazy('edit tournament', kwargs={'pk': self.request.user.player.team.tournament.id})


class SearchTournaments(ListView, LoginRequiredMixin):
    model = Tournament
    template_name = 'tournament/search_tournament.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        context['player'] = player
        return context


class JoinTournamentSearchResultsView(ListView, LoginRequiredMixin):
    model = Tournament
    template_name = "tournament/search_tournament_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Tournament.objects.filter(
            Q(name__icontains=query)
        )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        context['player'] = player
        return context


@method_decorator(join_tournament_decorators, name='dispatch')
class JoinTournamentView(UpdateView):
    model = Team
    template_name = 'tournament/join_tournament_confirm.html'
    form_class = JoinTournamentForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        context['player'] = player
        return context

    def get_success_url(self):
        return reverse_lazy('show home')


@login_required(redirect_field_name='show start')
@captaincy_required(redirect_field_name='show start')
@tournament_required(redirect_field_name='show start')
def leave_tournament(request, pk):
    player = Player.objects.get(pk=request.user.id)
    team = player.team
    if request.method == 'POST':
        if not player.is_tournament_creator:
            form = LeaveTournamentForm(request.POST, request.FILES, instance=team)
            if form.is_valid():
                team.tournament = None
                form.save()
                return redirect('show home')
        else:
            form = LeaveTournamentCreatorForm(request.POST, request.FILES, instance=team.tournament)
            if form.is_valid():
                team.tournament = None
                form.save()
                return redirect('show home')
    else:
        form = LeaveTournamentForm(instance=team)
    context = {
        'form': form,
        'player': player,
        'team': team,
    }
    return render(request, 'tournament/leave_tournament_confirm.html', context)
