from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from views import anonymousRequest, DataForwardView, ManageTimeslotsViewView, login, logout, main, courseSettings, courseDelete, CourseListView, RequestTimeslotView, ServerControlView, serverControlActivity, downloadFiles, deleteSchedule, zipRecording, imageGallery
from django.contrib.auth.decorators import login_required
#from tud_styling.views import *


urlpatterns = [

    # voor onderstaande url zie:  http://127.0.0.1:8000/static/x.html    (zo niet gebruiken)
    url(r'^forward/', DataForwardView.as_view(), name='forward'),

    url(r'^$', main, name='main'),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^request/$', anonymousRequest, name='request'),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    url(r'^course/list/$', login_required(CourseListView.as_view()), name='course-list'),
    url(r'^course/new/$', courseSettings, name='course-new'),
    url(r'^course/edit/(?P<courseId>[0-9]+)/$', courseSettings, name='course-edit'),
    url(r'^course/delete/(?P<courseId>[0-9]+)/$', courseDelete, name='course-delete'),

    url(r'^managetimeslots/(?P<courseId>[0-9]+)/$', login_required(ManageTimeslotsViewView.as_view()), name='managetimeslots'),
    url(r'^requesttimeslot/(?P<courseId>[0-9]+)/$', login_required(RequestTimeslotView.as_view()), name='requesttimeslot'),

    url(r'^servercontrol/$', ServerControlView.as_view(), name='servercontrol'),
    url(r'^serveractivity/ctrl/$', serverControlActivity, name='serveractivityctrl'),
    url(r'^files/deleteschedule/(?P<fileId>.*)/$', deleteSchedule, name='delete_schedule'),

    url(r'^files/$', downloadFiles, name='downloadFiles'),
    url(r'^files/ziprecording/(?P<fileId>.*)/$', zipRecording, name='zip_recording'),
    
    url(r'^images/(?:(?P<pid>.*)/)?$', imageGallery, name='image_gallery'),
    #url(r'^images/$', imageGallery, name='image_gallery'),
    #url(r'^images/(?P<pid>.*)/$', imageGallery, name='image_gallery_img'),
    
    # onderstaande is slechts ter demonstratie van sitetree menu in tud huisstijl
    url(r'^menutest/.*$', login_required(CourseListView.as_view()), name='menutest'),
]
