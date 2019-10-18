"""

        TRIP_APP URLS.py
"""


from django.conf.urls import url,include 
from .import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^success$',views.success),
    url(r'^dashboard$', views.dashboard),
    url(r'^trips/new$', views.new_trip),
    url(r'^trips/process_new$', views.process_new),
    url(r'^trips/process_edit$', views.process_edit),
    url(r'^trips/edit/(?P<trip_id>\d+)$', views.edit_trip),
    url(r'^trips/delete/(?P<trip_id>\d+)$', views.delete_trip),
    url(r'^trips/(?P<trip_id>\d+)$',views.show_trip),
    url(r'^trips/join/(?P<trip_id>\d+)$',views.join_trip),
    url(r'^trips/cancel/(?P<trip_id>\d+)$',views.cancel_trip),
    #url(r'^.*$',views.handle_page_not_found_404),
    
]
