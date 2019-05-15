from django.conf.urls import include, url

from django.contrib import admin

from MovieDB import views


urlpatterns = [#url('','MovieDB.views.home'),
                       url(r'^$', views.index),
                       #url(r'^listmovie/.*$', views.list_all),
                       # url(r'^addmovieform/$', views.add_movie_form),
                       url(r'^detail_movie/(?P<value>\d+)/$',views.get_movie_details,name='detail_movie'),
                       url(r'^searchmovie/$', views.search_movies),
                       url(r'^admin/', include(admin.site.urls)),
                       ]