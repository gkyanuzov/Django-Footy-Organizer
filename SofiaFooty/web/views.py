import datetime
from urllib import request

import django_tables2
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views_p here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# from SAL.web.models import Player, Team
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, TemplateView, RedirectView, ListView, UpdateView

from SofiaFooty.web.decorators import no_team_required, captaincy_required
from SofiaFooty.web.forms import ProfileForm, TeamCreationForm, TournamentCreationForm, DeleteProfileForm, JoinTeamForm, \
    LeaveTeamForm
from SofiaFooty.web.models import Player, Team, Tournament, SofiaFootyUser



# def create_profile(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('show index')
#     else:
#         form = UserCreationForm()
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'sign-up.html', context)
#
#
# @login_required(redirect_field_name='show start')
# def delete_profile(request):
#     # profile = Player.objects.get(pk=request.user.id)
#     if request.method == 'POST':
#         form = DeleteProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('show start')
#     else:
#         form = DeleteProfileForm(instance=request.user)
#     context = {
#         'form': form,
#     }
#     return render(request, 'profile/profile_delete.html', context)


@login_required(redirect_field_name='show start')
def show_home(request):
    player = Player.objects.get(pk=request.user.id)
    try:
        team = player.team
    except Team.DoesNotExist:
        team = None

    tournaments = Tournament.objects.all()
    upcoming_t = []
    active_t = []
    for t in tournaments:
        if t.is_started and t.end_date >= datetime.date.today():
            if len(active_t) >= 8:
                break
            active_t.append(t)
        elif not t.is_started:
            if len(upcoming_t) >= 8:
                break
            upcoming_t.append(t)

    sorted_active_tournaments = sorted(active_t, key=lambda t: t.start_date)
    sorted_upcoming_tournaments = sorted(upcoming_t, key=lambda t: t.start_date)

    context = {
        'team': team,
        'player': player,
        'upcoming_tournaments': sorted_upcoming_tournaments,
        'active_tournaments': sorted_active_tournaments,

    }
    return render(request, 'home.html', context)


def show_start_nologin(request):
    return render(request, 'start_page_nologin.html', )


# class HomeView(TemplateView):
#     template_name = 'home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

def show_public(request):
    tournaments = Tournament.objects.all()
    upcoming_t = []
    active_t = []
    for t in tournaments:
        if t.is_started and t.end_date >= datetime.date.today():
            if len(active_t) >= 8:
                break
            active_t.append(t)
        elif not t.is_started:
            if len(upcoming_t) >= 8:
                break
            upcoming_t.append(t)

    sorted_active_tournaments = sorted(active_t, key=lambda t: t.start_date)
    sorted_upcoming_tournaments = sorted(upcoming_t, key=lambda t: t.start_date)

    context = {
        'upcoming_tournaments': sorted_upcoming_tournaments,
        'active_tournaments': sorted_active_tournaments,

    }
    return render(request, 'public.html', context)
#
#
# class UserRegisterView(CreateView):
#     form_class = ProfileForm
#     template_name = 'profile/profile_create.html'
#     success_url = reverse_lazy('show index')
#
#
# class UserLoginView(LoginView):
#     template_name = 'start_page_nologin.html'
#     success_url = reverse_lazy('show index')
#
#     def get_success_url(self):
#         if self.success_url:
#             return self.success_url
#         return super().success_url()
#
#
# class UserLogoutView(LogoutView):
#     next_page = 'start_page_nologin.html'
#     # success_url = reverse_lazy('show start')
#
#
# create_team_decorators = [login_required, no_team_required]
#
#
# @method_decorator(create_team_decorators, name='dispatch')
# class CreateTeamView(CreateView):
#     form_class = TeamCreationForm
#     template_name = 'team/create_team.html'
#     success_url = reverse_lazy('show index')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#
#
#
# @method_decorator(login_required, name='dispatch')
# class ProfileDetailsView(DetailView):
#     model = Player
#     template_name = 'profile/profile_details.html'
#     context_object_name = 'player'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
#
# class TeamDetailsView(LoginRequiredMixin, DetailView):
#     model = Team
#     template_name = 'team/team_details.html'
#     context_object_name = 'team'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         player = Player.objects.get(pk=self.request.user.id)
#         players = Player.objects.filter(team__id= self.object.id)
#         context['player'] = player
#         context['players'] = players
#         context['is_captain'] = self.request.user.id == self.object.captain_id
#         return context
#
# @no_team_required  # stops users from manually typing join team link if they have a team already
# def join_team(request):
#     teams = Team.objects.all()
#     context = {
#         'teams': teams,
#     }
#     return render(request, 'team/search_team.html', context)
#
#
# class JoinTeamSearchResultsView(ListView):
#     model = Team
#     template_name = "team/search_team_results.html"
#
#     def get_queryset(self):  # new
#         query = self.request.GET.get("q")
#         object_list = Team.objects.filter(
#             Q(name__icontains=query)
#         )
#         return object_list
#
#
# class JoinTeamView(UpdateView):
#     model = Player
#     template_name = 'team/join_team_confirm.html'
#     form_class = JoinTeamForm
#
#     def get_success_url(self):
#         return reverse_lazy('show index')
#
#
# def leave_team(request, pk):
#     player = Player.objects.get(pk=request.user.id)
#     if request.method == 'POST':
#         form = LeaveTeamForm(request.POST, request.FILES, instance=player)
#         if form.is_valid():
#             player.team = None
#             form.save()
#             return redirect('show index')
#     else:
#         form = LeaveTeamForm(instance=player)
#     context = {
#         'form': form,
#         'player': player,
#     }
#     return render(request, 'team/leave_team_confirm.html', context)
#
#
# @method_decorator(captaincy_required, name='dispatch')
# class CreateTournamentView(CreateView):
#     form_class = TournamentCreationForm
#     template_name = 'tournament/create_tournament.html'
#     success_url = reverse_lazy('show index')
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#
# class TournamentDetailsView(DetailView):
#     pass
