from django.conf.urls import url
from django.contrib import admin

from django_encrypted_filefield.constants import FETCH_URL_NAME

from .views import MyDetailView, MyFetchView, MyFormView


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^detail/(?P<pk>\d+)$", MyDetailView.as_view(), name="detail"),
    url(r"^$", MyFormView.as_view(), name="index"),
    # This URL has to exist somewhere with this pattern and this name.  The
    # view used is up to you.
    url(r"^fetch/(?P<path>.+)", MyFetchView.as_view(), name=FETCH_URL_NAME),
]
