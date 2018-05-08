from django.conf.urls import url
from . import views
from .views import IndexView, TemplateView, Post_Detail_View, UserView, Post_Add_View, View,Post_Create_View
from django.contrib.auth.decorators import login_required 
# 通用视图直接在链接处加入login_required
# 正则只负责生产链接，实际的作用操作由后面的方法实现， name作为html链接后台方法关键字
urlpatterns = [
    # url(r'^$', views.post_list),
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^post/(?P<pk>[0-9]+)/$',
        Post_Detail_View.as_view(), name='post_detail'),
    # url(r'^category/(?P<pk>[0-9]+)/$', category-detail-view.as_view(),name="category_postlist"),
    url(r'^post/add/$', login_required(Post_Add_View.as_view()), name='post_new'),
    url(r'^post/create/$', login_required(Post_Create_View.as_view()), name='post_create'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$',
        views.post_publish, name='post_publish'),
    url(r'^user/(?P<slug>\w+)$', UserView.as_view(), name='user-view'),
    # url(r'^forgetpassword/$',
    #     TemplateView.as_view(template_name="beio_auth/forgetpassword.html"),
    #     name='forgetpassword-view'),
    url(r'^post/edit/(?P<pk>[0-9]+)$', views.post_edit, name='post_edit'),
    url(r'^post/reve/(?P<pk>[0-9]+)$', views.post_remove, name='post_remove'),
]
