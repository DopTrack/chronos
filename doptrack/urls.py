from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.decorators import login_required
# from tud_styling.views import *
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'^cms/', include('cms.urls')),

    url(r'^', include('doptrack_app.urls')),
    

    # deze kan na inbouwen huisstijl weg
    # url(r'^demo/', include('tud_styling.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
