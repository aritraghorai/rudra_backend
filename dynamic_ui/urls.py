from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProfileByPageNameView

router = DefaultRouter()
router.register(r"pages", ProfileViewSet)  # Keep existing CRUD APIs

urlpatterns = [
    path("/", include(router.urls)),
    path(
        "page/<str:page_name>/",
        ProfileByPageNameView.as_view(),
        name="page-by-page-name",
    ),
]
