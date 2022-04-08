from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from SofiaFooty.web.decorators import captaincy_required, no_tournament_required
from SofiaFooty.web.forms import TournamentCreationForm, JoinTournamentForm, LeaveTournamentForm
from SofiaFooty.web.models import Tournament, Player, Team, SofiaFootyUser

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
        context['teams'] = teams
        context['player'] = player
        context['is_creator'] = player.is_tournament_creator == True
        context['creator'] = creator
        print(player.is_tournament_creator)
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
