from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, FormView

from .forms import SignUpForm, SignInForm


class SignUpView(CreateView):
    model = get_user_model()
    form_class = SignUpForm


class SignInView(FormView):
    form_class = SignInForm
    template_name = 'auth/signin_form.html'
