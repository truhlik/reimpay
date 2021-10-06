from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from main.apps.core.views import run_cron_view

schema_view_ya = get_schema_view(
   openapi.Info(
      title="Reimpay API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
sitemaps_dict = {

}

urlpatterns = [
    # tyhle view handluje front a jsou zde jen dummy pro reverse url
    path('app/#/auth/login/', TemplateView.as_view(template_name='frontend.html'), name='login'),
    path('app/#/auth/new-password/', TemplateView.as_view(template_name='frontend.html'), name='frontend_password_reset'),
    path('app/#/patient/<int:pk>/', TemplateView.as_view(template_name='frontend.html'), name='frontend-patient-detail'),

    # tady už jsou backend URL
    path('accounts/', include('allauth.urls')),
    path('api/v1/', include('main.libraries.urls')),
    path('api/v1/', include('main.api_urls')),
    path('api/v1/accounts/', include('rest_auth.urls')),

    # yet another swagger gen
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_ya.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_ya.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/run-crons/', login_required(run_cron_view), name='admin-run-cron'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
