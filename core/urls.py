from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings
from . import views

app_name = 'core'
urlpatterns = [
    url('index', views.index ,name = 'index'),
    url('index/(?P<query>\s+)/$', views.index),
    url('syncpage', views.sync, name = 'syncpage'),
    url('faq', views.faq, name = 'faq'),
    url('installation', views.installation, name = 'installation'),
    url('sync', views.sync),
    url('activation', views.activation ,name = 'activation'),
    url('billing', views.billing ,name = 'billing'),
    url('shopdeletion', views.shopdeletion ,name = 'shopdeletion'),
    url('customerdeletion', views.customerdeletion ,name = 'customerdeletion'),
    url('webhooks', views.orders_create ,name = 'webhook'),
    url('datarequest', views.datarequest ,name = 'datarequest'),
    url('uninstall', views.app_uninstalled ,name = 'uninstall'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
