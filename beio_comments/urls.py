from django.conf.urls import url
from .views import CommentControl
# from . import views
urlpatterns = [

        # url(r'^comment/(?P<slug>\w+)$', CommentControl.as_view()),
        # url(r'^$',IndexView.as_view()),
         url(r'^comment/(?P<slug>[0-9]+)$',CommentControl.as_view(),name='commentajax'),
]
