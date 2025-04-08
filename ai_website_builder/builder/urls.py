# builder/urls.py (or websites/urls.py)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.shortcuts import redirect
from .views import (
    WebsiteViewSet,
    WebsiteCRUDView,
    PreviewWebsiteView,
    preview_website,
    register_view,
    login_view,
    logout_view,
    dashboard_view,
    create_website_view,
    preview_user_website,
    delete_website,
    update_content_view
)

router = DefaultRouter()
router.register(r'websites', WebsiteViewSet, basename='website')

urlpatterns = [
    # API endpoints
    path("", lambda request: redirect("dashboard")),
    path("api/", include(router.urls)),
    path("api/create/", WebsiteCRUDView.as_view(), name="create_via_api"),
    path("api/preview/<uuid:token>/", PreviewWebsiteView.as_view(), name="preview_token_api"),
    path('delete/<uuid:website_id>/', delete_website, name='delete_website'),
    path('website/<str:website_id>/edit/', update_content_view, name='edit_website'),
    # Frontend-rendered views
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("create-website/", create_website_view, name="create_website"),
     path('preview/<uuid:preview_token>/', preview_user_website, name='preview'),
    path("preview-token/<str:token>/", preview_website, name="preview_token_website"),
]
