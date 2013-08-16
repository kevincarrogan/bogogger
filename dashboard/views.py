from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, RedirectView):
    template_name = 'dashboard/dashboard.html'

    def get_redirect_url(self):
        return reverse('player_group_list')
