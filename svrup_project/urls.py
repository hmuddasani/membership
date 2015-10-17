"""svrup_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    	url(r'^$', "signup.views.home", name='home'),
		url(r'^register/$',"signup.views.register", name='register'),
        url(r'^projects/$', "videos.views.category_list", name='category_list'),
		url(r'^projects/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='category_detail'),
		url(r'^projects/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),
        url(r'^login/$', "svrup_project.views.auth_login", name='login'),
        url(r'^logout/$', "svrup_project.views.auth_logout", name='logout'),
		url(r'^comments/(?P<id>\d+)/$', "comments.views.comment_thread", name='comment_thread'),
		url(r'^comments/create/$', "comments.views.comment_create_view", name='comment_create_view'),
		url(r'^notifications/$', "notifications.views.all", name='notifications_all'),
		url(r'^notifications/(?P<id>\d+)/$', "notifications.views.read", name='notifications_read'),
		url(r'^notifications/unread/$', "notifications.views.all", name='notifications_unread'),
		url(r'^admin/', include(admin.site.urls)),
		url(r'^accounts/', include('registration.backends.default.urls')),
]
