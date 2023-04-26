from django.conf import settings
from django.urls import include, path 
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from rest_framework.authtoken import views as auth_views

from search import views as search_views
from users import urls as users_urls
from .api import api_router


# Change from the default name on the django admin site
admin.site.site_header = "DCTP Learning Platform"
admin.site.site_title = "Learning Platform"


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("users/", include(users_urls)),
    path("search/", search_views.search, name="search"),
    path("api/v1/token-auth", auth_views.obtain_auth_token),
    path("api/v1/", api_router.urls),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    path("", include(wagtail_urls)),
]
