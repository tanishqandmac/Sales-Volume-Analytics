from django.conf.urls import include, url
from core import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('login/', include('shopify_auth.urls')),
    url('', include('core.urls')),
    url('django-rq/', include('django_rq.urls')),
]
