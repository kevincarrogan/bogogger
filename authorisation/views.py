from django.contrib.auth import get_user_model, login, authenticate
from django.views.generic.edit import CreateView, FormView
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from .forms import SignUpForm, SignInForm, SignOutForm


class SignUpView(CreateView):
    model = get_user_model()
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('dashboard')

    def form_valid(self, form):
        user = form.instance
        data = form.cleaned_data

        resp = super(SignUpView, self).form_valid(form)

        authed_user = authenticate(username=user.username, password=data['password'])
        login(self.request, authed_user)

        return resp


class SignInView(FormView):
    form_class = SignInForm
    template_name = 'authorisation/signin_form.html'

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super(SignInView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard')


class SignOutView(FormView):
    form_class = SignOutForm
    template_name = 'authorisation/signout_form.html'

    def form_valid(self, form):
        logout(self.request)
        return super(SignOutView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard')

