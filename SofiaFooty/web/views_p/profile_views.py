from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView

from SofiaFooty.web.forms import DeleteProfileForm, ProfileForm, EditProfileForm
from SofiaFooty.web.models import Player, Team


class UserRegisterView(CreateView):
    form_class = ProfileForm
    template_name = 'profile/profile_create.html'
    success_url = reverse_lazy('show home')


class UserLoginView(LoginView):
    template_name = 'start_page_nologin.html'
    success_url = reverse_lazy('show home')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().success_url()


class UserLogoutView(LogoutView):
    next_page = 'start_page_nologin.html'
    # success_url = reverse_lazy('show start')


@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = Player
    template_name = 'profile/profile_edit.html'
    form_class = EditProfileForm
    context_object_name = 'player'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user.id})


@login_required(redirect_field_name='show start')
def delete_profile(request):
    # profile = Player.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = DeleteProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('show start')
    else:
        form = DeleteProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'profile/profile_delete.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileDetailsView(DetailView):
    model = Player
    template_name = 'profile/profile_details.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
