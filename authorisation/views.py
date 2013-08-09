from django.contrib.auth import get_user_model, login
from django.views.generic.edit import CreateView, FormView
from django.core.urlresolvers import reverse

from .forms import SignUpForm, SignInForm


class SignUpView(CreateView):
    model = get_user_model()
    form_class = SignUpForm


class SignInView(FormView):
    form_class = SignInForm
    template_name = 'authorisation/signin_form.html'

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return super(SignInView, self).form_valid(form)

    def get_success_url(self):
        return reverse('game_list')
