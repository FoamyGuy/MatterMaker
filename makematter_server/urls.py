from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from makematter_server import settings

admin.autodiscover()

urlpatterns = patterns(
        '',
        url(r'^$', 'makematter_server.views.index', name='index'),
        url(r'^make_box/', 'makematter_server.views.make_box', name='make_box'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
