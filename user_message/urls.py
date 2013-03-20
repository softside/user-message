from django.conf.urls import patterns, include, url
from django.contrib import admin
from message import views as messages_views
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',login_required(messages_views.MessageListView.as_view())),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^message/', include('message.urls')),
)
