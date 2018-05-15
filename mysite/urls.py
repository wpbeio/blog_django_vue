"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import  TemplateView
import xadmin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'', include('beio_blog.urls')),
    url(r'', include('beio_comments.urls')),
    url(r'', include('beio_auth.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),

    # url(r'', include('beio_comments.urls')),
    # url(r'^accounts/login/$', auth_views.login, name='login'),
    # url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    # url(r'^inbox/notifications/', include('notifications.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
