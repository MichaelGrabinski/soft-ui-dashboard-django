from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('testPage', views.webpage1, name='testPage'),
    path('Search', views.Search, name='Search'),
    path('Home', views.Home, name='Home'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', views.chart, name='chart')
   # path('form_page', views.form_page, name='form_page'),
]
