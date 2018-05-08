from django.conf.urls import url
from beio_auth.views import UserControl
from .import views


urlpatterns = [
    url(r'^usercontrol/(?P<slug>\w+)$', UserControl.as_view()),
    # url(r'down/down', views.big_file_download, name='down'),
]
