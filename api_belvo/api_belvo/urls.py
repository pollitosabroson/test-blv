from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.


apps_patterns = [
    url(r'^users', include('users.urls')),
]

# General api patterns
urlpatterns = [
    url(r'^api/v1/', include(apps_patterns)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
