from django.conf.urls import url
from django.contrib import admin

from .views import MyFormView, MyDetailView, MyFetchView

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    url(r"^detail/(?P<pk>\d+)$", MyDetailView.as_view(), name="detail"),
    url(r"^$", MyFormView.as_view(), name="index"),

    url(r"^fetch$", MyFetchView.as_view(), name="fetch"),

]
