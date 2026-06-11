"""
执法管理-案件质量-评查依据 URL 配置
"""
from django.urls import path, include
from rest_framework import routers

from app_reference.views import ReviewBasisViewSet

router = routers.SimpleRouter()
router.register(r"review-basis", ReviewBasisViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
