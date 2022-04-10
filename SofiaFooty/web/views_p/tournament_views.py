from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin

from SofiaFooty.web.decorators import captaincy_required, no_tournament_required
from SofiaFooty.web.forms import TournamentCreationForm, JoinTournamentForm, LeaveTournamentForm, MatchCreationForm, \
    EditMatchForm
from SofiaFooty.web.models import Tournament, Player, Team, SofiaFootyUser, Match

join_team_decorators = [captaincy_required, login_required, no_tournament_required()]


@method_decorator(captaincy_required, name='dispatch')
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


class TournamentDetailsView(DetailView):
    model = Tournament
    template_name = 'tournament/tournament_details.html'
    context_object_name = 'tournament'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        teams = Team.objects.filter(tournament_id=self.object.id)
        creator = self.object.creator.player
        matches = Match.objects.filter(tournament_id=self.object.id)
        context['teams'] = teams
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
        creator = self.object.creator.player
        context['teams'] = teams
        context['creator'] = creator
        return context


class TournamentTreeView(CreateView):
    model = Match
    form_class = MatchCreationForm
    template_name = 'tournament/tournament_tree.html'
    success_url = reverse_lazy('tournament tree')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if 'match_creation_form' not in kwargs:
        #     kwargs['match_creation_form'] = MatchCreationForm
        # if 'edit_match_form' not in kwargs:
        #     kwargs['edit_match_form'] = EditMatchForm
        palyer_id = self.request.user.id
        player = Player.objects.get(pk=palyer_id)
        team = player.team
        tournament = team.tournament
        matches = Match.objects.filter(tournament_id=tournament.id)
        context['player'] = player
        context['tournament'] = tournament
        context['matches'] = matches
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['player'] = Player.objects.get(pk= self.request.user.id)
        kwargs['tournament'] = Tournament.objects.get(pk= kwargs['player'].team.tournament.id)
        return kwargs

    # def post(self, request, *args, **kwargs):
    #     ctxt = {}
    #     if 'creation' in request.POST:
    #         match_creation_form = MatchCreationForm(request.POST, Player.objects.get(pk=request.user.id),
    #                                                 Tournament.objects.get(creator=self.request.user))
    #         if match_creation_form.is_valid():
    #             match_creation_form.save()
    #         else:
    #             ctxt['match_creation_form'] = match_creation_form
    #
    #     elif 'edit' in request.POST:
    #         edit_match_form = EditMatchForm(request.POST)
    #
    #         if edit_match_form.is_valid():
    #             edit_match_form.save()
    #         else:
    #             ctxt['edit_match_form'] = edit_match_form
    #
    #     return render(request, self.template_name, self.get_context_data(**ctxt))






# def tournament_tree_view(request, pk):
#     player = Player.objects.get(pk=request.user.id)
#     team = player.team
#     tournament = team.tournament
#
#     if request.method == 'POST':
#         form = MatchCreationForm(request.POST,  instance=team)
#         if form.is_valid():
#             team.tournament = None
#             form.save()
#             return redirect('show home')
#     else:
#         form = LeaveTournamentForm(instance=team)
#     context = {
#         'form': form,
#         'player': player,
#         'team': team,
#     }
#     return render(request, 'tournament/leave_tournament_confirm.html', context)



@no_tournament_required  # stops users from manually typing join team link if they have a team already
def search_tournament(request):
    tournaments = Tournament.objects.all()
    player = Player.objects.get(pk=request.user.id)
    context = {
        'tournaments': tournaments,
        'player': player,
    }
    return render(request, 'tournament/search_tournament.html', context)


class JoinTournamentSearchResultsView(ListView):
    model = Tournament
    template_name = "tournament/search_tournament_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Tournament.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


@method_decorator(join_team_decorators, name='dispatch')
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


def leave_tournament(request, pk):
    player = Player.objects.get(pk=request.user.id)
    team = player.team
    if request.method == 'POST':
        form = LeaveTournamentForm(request.POST, request.FILES, instance=team)
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
