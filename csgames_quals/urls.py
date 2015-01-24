from django.conf.urls import patterns, include, url
from django.contrib import admin
from csgames_quals import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^participant/(?P<id>\d+)$', views.participant_details, name='participant'),
    url(r'^competition/(?P<id>\d+)$', views.competition_details, name='competition'),
    url(r'^assign/(?P<competition_id>\d+)/(?P<participant_id>\d+)$', views.assign_participant, name='assign'),
    url(r'^schedule', views.schedule, name='schedule'),

    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
