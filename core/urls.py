from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from . import views

app_name = 'core'
urlpatterns = [
    url('index', views.index ,name = 'index'),
    url('index/(?P<query>\s+)/$', views.index),
    url('sync', views.sync),
    url('webhooks', views.orders_create ,name = 'webhook'),
    url('uninstall', views.app_uninstalled ,name = 'uninstall'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
