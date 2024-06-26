from django.contrib.auth import views as auth_views, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic import DeleteView

from DjigitAuto.accounts.forms import DjigitAutoCreationUserForm
from DjigitAuto.accounts.models import DjigitAutoUser, Profile
from DjigitAuto.offers.models import CarOffer


class ReadOnlyMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        for field in form.fields.values():
            field.widget.attrs["readonly"] = "readonly"

        return form


class SignInUserView(auth_views.LoginView):
    template_name = "accounts/sign-in.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')


class SignUpUserView(views.CreateView):
    template_name = 'accounts/sign-up.html'
    form_class = DjigitAutoCreationUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, form.instance)

        return result


class ProfileDetailsView(views.DetailView):
    queryset = Profile.objects.prefetch_related("user").all()
    template_name = 'accounts/profile-details.html'


class ProfileUpdateView(views.UpdateView):
    queryset = Profile.objects.all()
    template_name = 'accounts/edit-profile.html'
    fields = ("profile_picture", "first_name", "last_name", "age")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        car_offers = CarOffer.objects.filter(user=profile.user)
        context['car_offers'] = car_offers
        return context

    def get_success_url(self):
        return reverse('profile details', kwargs={
            'pk': self.object.pk,
        })


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "accounts/delete-profile.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return self.request.user


def signout_user(request):
    logout(request)
    return redirect('index')
