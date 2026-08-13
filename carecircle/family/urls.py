from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FamilyMemberViewSet

router = DefaultRouter()
router.register(r'members', FamilyMemberViewSet, basename='familymember')

urlpatterns = [
    path('', include(router.urls)),
]
