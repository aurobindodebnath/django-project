"""django_project URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from riddles import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),



    #loggedin/
    url(r'^loggedin/correct/(?P<user_id>[0-9]+)/(?P<riddle_id>[0-9]+)/$', views.correct, name='correct' ),
    url(r'^loggedin/wrong/(?P<user_id>[0-9]+)/(?P<riddle_id>[0-9]+)/$', views.wrong , name='wrong' ),

    url(r'^loggedin/$', views.loggedin , name="loggedin"),

    #loggedin/submissions/
    url(r'^loggedin/submissions/$', views.submissions, name="submissions"),
    
    #loggedin/123/submit/
    url(r'^loggedin/(?P<riddle_id>[0-9]+)/submit/$', views.submit, name="submit"),
    
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),


#    url(r'^loggedin/map/$', views.map , name="map"),
    url(r'^loggedin/standings/$', views.standings , name="standings"),
    url(r'^loggedin/shutdown/$', views.shutdown, name="shutdown"),
    url(r'^loggedin/sureshutdown/$', views.sureshutdown, name="sureshutdown"),
    url(r'^loggedin/start/$', views.start, name="start"),
    url(r'^loggedin/surestart/$', views.surestart, name="surestart"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)