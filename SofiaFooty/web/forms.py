import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.http import request

from SofiaFooty.web.helpers import BootstrapFormMixin
from SofiaFooty.web.models import Player, Team, Tournament, SofiaFootyUser, Match


# <------------------PROFILEFORMS------------------------>

class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(UserCreationForm, ):
    # refactor player model with class Attributes - example: Player Name Max Len etc.
    first_name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control'}),

    )

    image = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self._init_bootstrap_form_controls()
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].help_text = ''

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Player(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            image=self.cleaned_data['image'],
            email=self.cleaned_data['email'],
            age=self.cleaned_data['age'],
            user=user,
        )
        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'image', 'age', 'email')
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter first name'
        #         }
        #     ), 'last_name': forms.TextInput(
        #         attrs={
        #             'placeholder': 'Enter last name',
        #             'class': 'form-control',
        #
        #         }
        #     ), 'image': forms.URLInput(
        #         attrs={
        #             'placeholder': 'Enter URL'
        #         }
        #     )
        # }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ('user', 'is_captain', 'is_tournament_creator', 'team',)


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = SofiaFootyUser
        fields = ()


# <------------------TEAMFORMS------------------------>
class TeamCreationForm(forms.ModelForm, BootstrapFormMixin):
    # name = forms.CharField(
    #     max_length=25,
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    # )
    #
    # emblem = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))

    # description = forms.Textarea(widget=forms.Textarea(attrs={'class': 'form-control'}))

    # number_of_players = forms.ChoiceField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        team = super().save(commit=False)  # poluchava team instance
        team.captain = self.user
        p = Player.objects.get(pk=self.user.id)
        if commit:
            team.save()
            p.team = team
            p.is_captain = True
            p.save()
        return team

    class Meta:
        model = Team
        fields = ('name', 'emblem', 'description', 'number_of_players',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter team name',
                    'class': 'form-control'
                }
            ), 'emblem': forms.URLInput(
                attrs={
                    'placeholder': 'Insert emblem URL',
                    'class': 'form-control'
                },
            ), 'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter team description',
                    'class': 'form-control'
                },
            )
        }


class JoinTeamForm(forms.ModelForm):
    all_teams = Team.objects.all()
    available_teams = []
    for team in all_teams:
        if team.has_space:
            available_teams.append(team)
    available_teams_pk = [team.id for team in available_teams]
    team = forms.ModelChoiceField(queryset=Team.objects.filter(pk__in=available_teams_pk), label='')

    class Meta:
        model = Player
        fields = ('team',)


# ako iskash disablenato pole - widget=forms.Select(attrs={'disabled':'disabled'})
class LeaveTeamForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ()


class LeaveTeamCaptainForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ()

    def save(self, commit=True):
        player_captain = self.instance.captain.player
        player_captain.is_captain = False
        player_captain.save()
        self.instance.delete()
        return self.instance


# <------------------TOURNAMENTFORMS------------------------>
class TournamentCreationForm(forms.ModelForm, BootstrapFormMixin):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    # Validates if end date is greater than start date
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    def save(self, commit=True):
        tournament = super().save(commit=False)  # poluchava tournament instance
        tournament.creator = self.user
        p = Player.objects.get(pk=self.user.id)
        team = p.team
        p.is_tournament_creator = True
        p.current_tournament = tournament
        if commit:
            tournament.save()
            team.tournament = tournament
            team.save()
            p.is_tournament_creator = True
            p.current_tournament = tournament
            p.save()
        return tournament

    class Meta:
        model = Tournament
        fields = ('name', 'size', 'description', 'start_date', 'end_date')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter tournament name'
                }
            ),
            'start_date': DateInput(),
            'end_date': DateInput(),
        }


class JoinTournamentForm(forms.ModelForm):
    all_tournaments = Tournament.objects.all()
    available_tournaments = []
    for t in all_tournaments:
        if t.has_space:
            available_tournaments.append(t)
    available_tournaments_pk = [t.id for t in available_tournaments]
    tournament = forms.ModelChoiceField(queryset=Tournament.objects.filter(pk__in=available_tournaments_pk), label='')

    class Meta:
        model = Team
        fields = ('tournament',)


class LeaveTournamentForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ()


# <---------------MATCH FORMS---------->

class MatchCreationForm(forms.ModelForm):
    def __init__(self, user, player, tournament, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tournament = tournament
        self.player = player
        self.user = user
        self.fields['tournament'] = forms.ModelChoiceField(queryset=Tournament.objects.filter(pk=self.tournament.id))
        self.fields['home_team'] = forms.ModelChoiceField(
            queryset=Team.objects.filter(tournament_id=self.tournament.id).filter(continue_to_next_round=True))
        self.fields['away_team'] = forms.ModelChoiceField(
            queryset=Team.objects.filter(tournament_id=self.tournament.id).filter(continue_to_next_round=True))

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        home_team = cleaned_data.get("home_team")
        away_team = cleaned_data.get("away_team")
        tournament = cleaned_data.get("tournament")
        if date < datetime.date.today():
            raise forms.ValidationError("Match date should not before  today`s date.")

        if not tournament.start_date <= date <= tournament.end_date:
            raise forms.ValidationError("Match must be played within the tournaments period.")

        if home_team == away_team:
            raise forms.ValidationError("Please choose two different teams.")

    class Meta:
        model = Match
        exclude = ('home_team_goals', 'away_team_goals')
        widgets = {
            'date': DateInput(),
            'details': forms.Textarea(
                attrs={'placeholder': 'Add game details like starting hour, venue etc..'},
            )
        }

    def save(self, commit=True):
        match = super().save(commit=False)
        home_team = match.home_team
        away_team = match.away_team
        if commit:
            match.save()
            home_team.continue_to_next_round = False
            home_team.save()
            away_team.continue_to_next_round = False
            home_team.save()
            away_team.save()
            return match


class EditMatchForm(forms.ModelForm):
    home_team_goals = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    away_team_goals = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Add game details like goalscorers, game stats etc..'}))

    def clean(self):
        cleaned_data = super().clean()
        home_team_goals = cleaned_data.get("home_team_goals")
        away_team_goals = cleaned_data.get("away_team_goals")
        if home_team_goals == away_team_goals:
            raise forms.ValidationError(
                "There must be a winner from the match. You can add details, like penalties, replay score etc.. in the details tab below.")

    class Meta:
        model = Match
        fields = ('home_team_goals', 'away_team_goals', 'details',)

    def save(self, commit=True):
        match = super().save(commit=False)
        home_team = match.home_team
        away_team = match.away_team
        if commit:
            match.save()
            if match.home_team_goals > match.away_team_goals:
                home_team.continue_to_next_round = True
                home_team.save()
            else:
                away_team.continue_to_next_round = True
                away_team.save()
            return match


class EditMatchDetailsForm(forms.ModelForm):

    details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Add game details like goalscorers, game stats etc..'}))

    class Meta:
        model = Match
        fields = ('date', 'details',)
        widgets = {
            'date': DateInput(),
        }



