from rest_framework import routers
from django.urls import path, include
from app_personal_sacrifice.views import PersonalSacrificeViewSet

router = routers.SimpleRouter()
router.register(r'sacrifice', PersonalSacrificeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
