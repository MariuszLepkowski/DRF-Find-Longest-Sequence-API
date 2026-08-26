from django.urls import path

from core.views import ProcessDataAPIView

urlpatterns = [
    path(
        "api/process/",
        ProcessDataAPIView.as_view(),
        name="process-data",
    ),
]
