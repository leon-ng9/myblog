from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^posts/(?P<year>\d+)/(?P<month>\d+)/$', views.post_month, name='post_month'),

    url(r'^post/(?P<pk>\d+)/comment/$', views.post_add_comment, name='post_add_comment'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.post_comment_approve, name='post_comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.post_comment_delete, name='post_comment_delete'),

    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),

    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),

    url(r'', views.post_list, name='post_list'),
]