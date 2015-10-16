#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose:
Author: 'yac'
Date:
"""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from chat.views import error404, error500
import socketio.sdjango

admin.autodiscover()

urlpatterns = patterns('chat.views',
                       url(r'^chat', 'chat', name='broadcast_chat'),
                       url(r'^login', 'auth_and_login'),
                       url(r'^logout', 'logout_user'),
                       url(r'^signup', 'sign_up_in'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', RedirectView.as_view(url=reverse_lazy('broadcast_chat'))),
                       url(r'^socket\.io', include(socketio.sdjango.urls)),
                       )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
else:
    from django.views.static import serve
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    )

handler404 = error404
handler500 = error500