from django.urls import reverse_lazy
from django.views.generic import UpdateView

from SofiaFooty.web.forms import EditMatchForm, EditMatchDetailsForm
from SofiaFooty.web.models import Match, Player


class EditMatchView(UpdateView):
    model = Match
    template_name = 'match/edit_match.html'
    form_class = EditMatchForm
    success_url = reverse_lazy('manage tournament')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        context['player'] = player
        return context


class EditMatchDetailsView(UpdateView):
    model = Match
    template_name = 'match/edit_match_details.html'
    form_class = EditMatchDetailsForm
    success_url = reverse_lazy('manage tournament')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = Player.objects.get(pk=self.request.user.id)
        context['player'] = player
        return context