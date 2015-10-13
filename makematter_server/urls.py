from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from makematter_server import app_settings

admin.autodiscover()

urlpatterns = patterns(
        '',
        url(r'^$', 'makematter_server.views.index', name='index'),
        #url(r'^mtv/$', 'makematter_server.views.show_matter_template', name='mtv'),

        url(r'^render_matter_template/(?P<uuid>[0-Fa-f]{8}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{12})/$',
            'makematter_server.views.make_object.render_matter_template', name='RenderMatterTemplate'),

        url(r'^show_matter_template/(?P<uuid>[0-Fa-f]{8}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{12})/$',
            'makematter_server.views.show_matter_template', name='ShowMatterTemplate'),



        url(r'^make_box/', 'makematter_server.views.make_box', name='make_box'),
) + static(app_settings.MEDIA_URL, document_root=app_settings.MEDIA_ROOT)
