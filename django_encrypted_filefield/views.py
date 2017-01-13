import os

import requests

import magic
from django.conf import settings
from django.core.validators import URLValidator, ValidationError
from django.http import Http404, HttpResponse
from django.views.generic import View

from .crypt import Cryptographer


class FetchView(View):
    """
    This is a generic, insecure view that effectively undoes any security made
    available via this module.  To make it useful, you have to subclass it and
    make use of your own rules or simply rely on the auth mixins provided by
    Django:

      from django.contrib.auth.mixins import LoginRequiredMixin
      from django_encrypted_fields.views import FetchView as BaseFetchView

      class FetchView(LoginRequiredMixin, BaseFetchView):
          pass

    Using LoginRequiredMixin would effectively allow anyone with a site login
    to view *all* files, while using something like StaffRequiredMixin would
    mean that only staff members could read the file.

    Theoretically you could also write your view to be smart enough to take the
    requested path and match it against a list of permissions, allowing you to
    set out per-user permissions whilst still only using one encryption key for
    the whole site.

    """

    def get(self, request, *args, **kwargs):

        path = kwargs.get("path")

        # No path?  You're boned.  Move along.
        if not path:
            raise Http404

        if self._is_url(path):

            content = requests.get(path, stream=True).raw.read()

        else:

            # Normalise the path to strip out naughty attempts
            path = os.path.normpath(path).replace(
                settings.MEDIA_URL, settings.MEDIA_ROOT, 1)

            # Evil path request!
            if not path.startswith(settings.MEDIA_ROOT):
                raise Http404

            # The file requested doesn't exist locally.  A legit 404
            if not os.path.exists(path):
                raise Http404

            with open(path, "rb") as f:
                content = f.read()

        content = Cryptographer.decrypted(content)
        return HttpResponse(
            content, content_type=magic.Magic(mime=True).from_buffer(content))

    @staticmethod
    def _is_url(path):
        try:
            URLValidator()(path)
            return True
        except ValidationError:
            return False
