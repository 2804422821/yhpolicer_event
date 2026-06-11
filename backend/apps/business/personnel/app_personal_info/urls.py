from rest_framework import routers
from django.urls import path, include
from apps.business.personnel.app_personal_info.views import PersonalInfoViewSet

router = routers.SimpleRouter()
router.register(r'info', PersonalInfoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]