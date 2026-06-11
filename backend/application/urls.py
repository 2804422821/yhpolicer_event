"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.system.app_login.views import CaptchaView, LoginView

urlpatterns = [
    path('getCaptcha/', CaptchaView.as_view()),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path('admin/', admin.site.urls),
    path('system/', include('apps.system.app_post.urls')),
    path('system/', include('apps.system.app_dept.urls')),
    path('system/', include('apps.system.app_apis.urls')),
    path('system/', include('apps.system.app_menu.urls')),
    path('system/', include('apps.system.app_role.urls')),
    path('system/', include('apps.system.app_dict.urls')),
    path('system/', include('apps.system.app_user.urls')),
    path('system/', include('apps.infrastructure.app_operation_log.urls')),
    path('system/', include('apps.infrastructure.app_message.urls')),
    path('system/', include('app_example.urls')),
    path('enforcement/case-quality/', include('apps.business.app_reference.urls')),
    path('pension/people/', include('apps.business.personnel.app_personal_info.urls')),
    path('pension/people/', include('apps.business.personnel.app_personal_died.urls')),
    path('pension/people/', include('apps.business.personnel.app_personal_sacrifice.urls')),
    path('pension/people/', include('apps.business.personnel.app_personal_disability.urls')),
    path('job/crontab/', include('apps.infrastructure.app_crontab.urls')),
    path('tool/', include('apps.infrastructure.app_monitor.urls')),
]
