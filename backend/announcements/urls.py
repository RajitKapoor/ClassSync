"""
URLs for announcements app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'', AnnouncementViewSet, basename='announcement')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]

