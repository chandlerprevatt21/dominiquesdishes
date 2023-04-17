from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from base.views import home, story, service_detail, contact
from gallery.views import GalleryHome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('cart/', include(('carts.urls', 'carts'), namespace="carts")),
    path('contact/', contact, name="contact"),
    path('catering/', include(('catering.urls', 'catering'), namespace="catering")),
    path('gallery/', GalleryHome, name="gallery"),
    path('menus/', include(('menus.urls', 'menus'), namespace="menus")),
    path('story/', story, name="story"),
    path('services/<slug>/', service_detail, name="service-detail")
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

