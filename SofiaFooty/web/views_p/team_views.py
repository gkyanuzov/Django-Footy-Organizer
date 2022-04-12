import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from SofiaFooty.web.decorators import no_team_required
from SofiaFooty.web.forms import JoinTeamForm, LeaveTeamForm, TeamCreationForm, LeaveTeamCaptainForm
from SofiaFooty.web.models import Team, Player, Match

create_team_decorators = [login_required, no_team_required]


@method_decorator(create_team_decorators, name='dispatch')
class CreateTeamView(CreateView):
    form_class = TeamCreationForm
    template_name = 'team/create_team.html'
    success_url = reverse_lazy('show home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TeamDetailsView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'team/team_details.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        player = Player.objects.get(pk=self.request.user.id)
        players = Player.objects.filter(team__id= self.object.id)

        players_to_show = list(players)

        try:
            players_to_show = list(players)[0:5]
        except IndexError:
            players_to_show = players

        home_matches = Match.objects.filter(home_team=self.object)
        away_matches = Match.objects.filter(away_team=self.object)
        all_matches = sorted([m for m in list(home_matches)] + [m for m in list(away_matches)], key= lambda m: m.date)
        all_matches = [m for m in all_matches if m.date >= datetime.date.today()]

        try:
            all_matches = all_matches[0:7]
        except IndexError:
            all_matches = all_matches

        context['matches'] = all_matches
        context['player'] = player
        context['players'] = players
        context['players_to_show'] = players_to_show
        context['is_captain'] = self.request.user.id == self.object.captain_id
        return context


@no_team_required  # stops users from manually typing join team link if they have a team already
def search_team(request):
    teams = Team.objects.all()
    context = {
        'teams': teams,
    }
    return render(request, 'team/search_team.html', context)


class JoinTeamSearchResultsView(ListView):
    model = Team
    template_name = "team/search_team_results.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Team.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


@method_decorator(no_team_required, name='dispatch')
class JoinTeamView(UpdateView):
    model = Player
    template_name = 'team/join_team_confirm.html'
    form_class = JoinTeamForm

    def get_success_url(self):
        return reverse_lazy('show home')


def leave_team(request, pk):
    player = Player.objects.get(pk=request.user.id)
    if request.method == 'POST':
        if not player.is_captain:
            form = LeaveTeamForm(request.POST, request.FILES, instance=player)
            if form.is_valid():
                player.team = None
                form.save()
                return redirect('show home')
        else:
            form = LeaveTeamCaptainForm(request.POST, request.FILES, instance=player.team)
            if form.is_valid():
                player.is_captain = False
                form.save()
                return redirect('show home')
    else:
        form = LeaveTeamForm(instance=player)
    context = {
        'form': form,
        'player': player,
    }
    return render(request, 'team/leave_team_confirm.html', context)

