from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView

from .forms import SignUpForm


class SignUpView(CreateView):
    model = get_user_model()
    form_class = SignUpForm
