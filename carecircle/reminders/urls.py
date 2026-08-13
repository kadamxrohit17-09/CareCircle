from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FollowUpViewSet

router = DefaultRouter()
router.register(r'reminders', FollowUpViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
]
