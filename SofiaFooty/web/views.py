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
from SofiaFooty.web.models import Player, Team, Tournament, SofiaFootyUser, Match



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

    matches = Match.objects.filter(tournament__in=sorted_upcoming_tournaments)
    try:
        matches = sorted(matches[0:10], key=lambda m: m.date)
    except IndexError:
        matches = sorted(matches, key=lambda m: m.date)
    context = {
        'team': team,
        'player': player,
        'upcoming_tournaments': sorted_upcoming_tournaments,
        'active_tournaments': sorted_active_tournaments,
        'upcoming_matches': matches,

    }
    return render(request, 'home.html', context)


def show_start_nologin(request):
    return render(request, 'start_page_nologin.html', )


def show_public(request):
    tournaments = Tournament.objects.all()
    upcoming_t = []
    active_t = []
    for t in tournaments:
        if t.is_started and t.end_date >= datetime.date.today():
            if len(active_t) >= 8:
                break
            active_t.append(t)

    for t in tournaments:
        if not t.is_started:
            if len(upcoming_t) >= 8:
                break
            upcoming_t.append(t)

    sorted_active_tournaments = sorted(active_t, key=lambda t: t.start_date)
    sorted_upcoming_tournaments = sorted(upcoming_t, key=lambda t: t.start_date)
    matches = Match.objects.filter(tournament__in=sorted_upcoming_tournaments)
    try:
        matches = sorted(matches[0:10], key= lambda m: m.date)
    except IndexError:
        matches = sorted(matches, key= lambda m: m.date)

    context = {
        'upcoming_tournaments': sorted_upcoming_tournaments,
        'active_tournaments': sorted_active_tournaments,
        'matches': matches,

    }
    return render(request, 'public_home.html', context)


