import datetime
from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
# Create your models here.
from django.db.models import SET_NULL

# Create your models here.
from SofiaFooty.web.managers import SofiaFootyUserManager
import django_tables2 as tables


class SofiaFootyUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_MAX_LENGTH = 25
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'username'

    objects = SofiaFootyUserManager()


class Player(models.Model):
    PlAYER_FIRST_NAME_MIN_LEN = 4
    PlAYER_LAST_NAME_MIN_LEN = 4
    PLAYER_MIN_AGE = 14

    first_name = models.CharField(
        max_length=25,
        validators=(
            MinLengthValidator(PlAYER_FIRST_NAME_MIN_LEN),
        )
    )

    last_name = models.CharField(
        max_length=25,
        validators=(
            MinLengthValidator(PlAYER_LAST_NAME_MIN_LEN),
        )
    )

    email = models.EmailField(unique=True, )

    image = models.URLField(
        blank=True,
        null=True,
    )

    age = models.IntegerField(
        validators=(
            MinValueValidator(PLAYER_MIN_AGE),
        ),
    )

    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


    user = models.OneToOneField(
        SofiaFootyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    is_captain = models.BooleanField(
        default=False,
        blank=True,
        null=True,
    )

    is_tournament_creator = models.BooleanField(
        default=False,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Team(models.Model):
    TEAM_NAME_MIN_LEN = 4
    SIX_PLAYERS = '6'
    EIGHT_PLAYERS = '8'
    TEN_PLAYERS = '10'

    NUMBER_OF_PLAYERS = [(x, x) for x in (SIX_PLAYERS, EIGHT_PLAYERS, TEN_PLAYERS)]

    name = models.CharField(
        max_length=30,
        unique=True,
        validators=(
            MinLengthValidator(TEAM_NAME_MIN_LEN),
        )
    )

    emblem = models.URLField()

    description = models.TextField(
        max_length=150,
        blank=True,
        null=True,
    )

    number_of_players = models.CharField(
        max_length=3,
        choices=NUMBER_OF_PLAYERS,
    )

    # members = models.ManyToManyField(
    #     # TODO:Add abstraction with get user model()
    #     # TODO: validate if team is full
    #     SofiaFootyUser,
    #     related_name='members',
    #     blank=True,
    # )

    tournament = models.ForeignKey(
        'Tournament',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    captain = models.ForeignKey(SofiaFootyUser, on_delete=models.SET_NULL, null=True, blank=True, )

    def __str__(self):
        return f'{self.name}, Size:{self.number_of_players}'

    @property
    def has_space(self):
        players = list(Player.objects.filter(team_id=self.id))
        if len(players) < int(self.number_of_players):
            return True
        return False


class Tournament(models.Model):
    TOURNAMENT_NAME_MAX_LEN = 30

    EIGHT_TEAMS = '8'
    SiXTEEN_TEAMS = '16'
    THIRTY_TWO_TEAMS = '32'

    NUMBER_OF_TEAMS = [(x, x) for x in (EIGHT_TEAMS, SiXTEEN_TEAMS, THIRTY_TWO_TEAMS)]

    name = models.CharField(
        max_length=TOURNAMENT_NAME_MAX_LEN,
        unique=True,
    )

    size = models.CharField(
        max_length=3,
        choices=NUMBER_OF_TEAMS,
    )

    # teams = models.ManyToManyField(
    #     # TODO:Add abstraction with get user model()
    #     # TODO: validate if team is full
    #     Team,
    #     related_name='teams',
    #     blank=True,
    # )

    creator = models.ForeignKey(SofiaFootyUser, on_delete=models.SET_NULL, null=True, blank=True, )

    description = models.TextField(
        max_length=150,
        blank=True,
        null=True,
    )

    start_date = models.DateField(default=datetime.date.today(), )

    end_date = models.DateField(default=datetime.date.today(), )

    @property
    def is_started(self):
        return self.start_date <= datetime.date.today()

    @property
    def has_space(self):
        teams = list(Team.objects.filter(tournament_id=self.id))
        if len(teams) < int(self.size):
            return True
        return False

    def __str__(self):
        return f'{self.name}, Size:{self.size}'

    # matches


class Match(models.Model):
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='home_team',
    )

    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='away_team',
    )

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
    )

    home_team_goals = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        validators=(
            MinValueValidator(0),
        )
    )

    away_team_goals = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        validators=(
            MinValueValidator(0),
        )
    )

    date = models.DateField(default=date.today())

    def __str__(self):
        return f'{self.home_team.name} {self.home_team_goals}:{self.away_team_goals} {self.away_team.name}'
