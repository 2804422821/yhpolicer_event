from rest_framework import routers
from django.urls import path, include
from apps.business.personnel.app_personal_died.views import PersonalDiedViewSet

router = routers.SimpleRouter()
router.register(r'died', PersonalDiedViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
