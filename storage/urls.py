from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    re_path(r'^lsprj/$', views.lsProject, name='ls_prj'),

    re_path(r'^pview/(?P<id>\d+)/$', views.pView, name='pview'),
    re_path(r'^padd/$', views.pAdd, name='padd'),
    re_path(r'^pedit/(?P<id>\d+)/$', views.pEdit, name='pedit'),
    re_path(r'^pdel/(?P<id>\d+)/$', views.pDelete, name='pdel'),

    re_path(r'^fadd/(?P<pg_id>\d+)/$', views.fAdd, name='fadd'),


    re_path(r'^st/(?P<id>\d+)/$', views.del_load_Doc, name='streem_doc'),
]