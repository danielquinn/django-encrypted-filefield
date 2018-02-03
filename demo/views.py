try:
    from django.urls import reverse
except ImportError:
    # Django < v2.0
    from django.core.urlresolvers import reverse

from django.views.generic import CreateView, DetailView

from django_encrypted_filefield.views import FetchView

from .forms import MyForm
from .models import MyModel


class MyFormView(CreateView):
    form_class = MyForm
    template_name = "demo/index.html"

    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.object.pk})


class MyDetailView(DetailView):
    model = MyModel
    template_name = "demo/detail.html"


class MyFetchView(FetchView):
    """
    This really should be using a mixin like LoginRequiredMixin.  See the
    parent class for more information.
    """
    pass
