from rest_framework import routers
from django.urls import path, include
from apps.business.personnel.app_personal_disability.views import PersonalDisabilityViewSet

router = routers.SimpleRouter()
router.register(r'disability', PersonalDisabilityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
