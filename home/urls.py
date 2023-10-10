from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('Home', views.index, name='index'),
    path('Tolland', views.Tolland, name='Tolland'),
    path('EHMS', views.EHMS, name='EHMS'),
    path('EHHS', views.EHHS, name='EHHS'),
    path('testPage', views.webpage1, name='testPage'),
    path('Search', views.Search, name='Search'),
    path('', views.Home, name='Home'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('low_quantity_parts/', views.low_quantity_parts, name='low_quantity_parts'),
    path('filtered_inventory_changes/', views.filtered_inventory_changes, name='filtered_inventory_changes'),
    path('logout/', views.logout_view, name='logout'),
    path('ML_Page/', views.ml_view, name='ML_Page'),
   # path('', views.chart, name='chart')
   # path('form_page', views.form_page, name='form_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
