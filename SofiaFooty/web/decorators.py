from django.contrib.auth.decorators import user_passes_test

from SofiaFooty.web.models import Player, Team


# stops users from manually typing join team link if they have a team already
def no_team_required(function=None, redirect_field_name='show index'):
    def has_no_team(u):
        p = Player.objects.get(user_id=u.id)
        return  p.team == None

    actual_decorator = user_passes_test(has_no_team, redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator


def team_required(function=None, redirect_field_name='show index'):
    def has_team(u):
        p = Player.objects.get(user_id=u.id)
        return p.team != None

    actual_decorator = user_passes_test(has_team, redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator


def no_tournament_required(function=None, redirect_field_name='show index'):
    def has_no_tournament(u):
        p = Player.objects.get(user_id=u.id)
        t = p.team
        return t.tournament == None

    actual_decorator = user_passes_test(has_no_tournament, redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator


def tournament_required(function=None, redirect_field_name='show index'):
    def has_tournament(u):
        p = Player.objects.get(user_id=u.id)
        t = p.team
        return t.tournament != None

    actual_decorator = user_passes_test(has_tournament, redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator

def captaincy_required(function=None, redirect_field_name='show index'):
    def is_captain(u):
        p = Player.objects.get(user_id=u.id)
        return p.is_captain
    actual_decorator = user_passes_test(is_captain, redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator


def tournament_creator_required(function=None, redirect_field_name='show index'):
    def is_creator(u):
        p = Player.objects.get(user_id=u.id)
        return p.is_tournament_creator
    actual_decorator = user_passes_test(is_creator, redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator


