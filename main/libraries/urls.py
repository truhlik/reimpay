from django.urls import path

from main.libraries.api_views import AresView


urlpatterns = [
    path('ares/company/', AresView.as_view(), name='ares'),
]
