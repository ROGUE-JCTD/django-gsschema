from django.conf.urls import patterns, include, url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_gsschema_prj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^gsschema/', include('gsschema_prj.gsschema.urls')),
    (r'^$', RedirectView.as_view(url='/gsschema/list/')),

    url(r'^admin/', include(admin.site.urls)),
)
