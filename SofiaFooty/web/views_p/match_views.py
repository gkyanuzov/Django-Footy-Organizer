from django.urls import reverse_lazy
from django.views.generic import UpdateView

from SofiaFooty.web.forms import EditMatchForm
from SofiaFooty.web.models import Match


class EditMatchView(UpdateView):
    model = Match
    template_name = 'match/edit_match.html'
    form_class = EditMatchForm
    success_url = reverse_lazy('manage tournament')
