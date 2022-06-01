from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = i18n_patterns = [
    url(r'^social_media/$', views.demo_social_media, name="social_media"),
    url(r'^form/$', views.demo_form, name="form"),
    url(r'^form_template/$', views.demo_form_with_template, name="form_template"),
    url(r'^form_inline/$', views.demo_form_inline, name="form_inline"),
    url(r'^formset/$', views.demo_formset, name="formset"),
    url(r'^tabs/$', views.demo_tabs, name="tabs"),
    url(r'^table/$', views.demo_table, name="table"),
    url(r'^accordion/$', views.demo_accordion, name="accordion"),
    url(r'^pagination/$', views.demo_pagination, name="pagination"),
    url(r'^jquery-ui/$', TemplateView.as_view(template_name='demo/jquery-ui.html'), name="jquery-ui"),
]
