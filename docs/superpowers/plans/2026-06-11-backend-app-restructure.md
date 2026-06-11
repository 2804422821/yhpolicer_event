# Backend App 目录重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 backend 下 20 个 app_* 目录按业务域分组到 apps/system/、apps/business/、apps/infrastructure/ 子目录中，不影响系统正常运行

**Architecture:** 使用 `git mv` 物理移动目录；修改 `AppConfig.name` 为完整 Python 路径但保持 `label`（末段）不变，确保数据库和迁移无需改动；更新所有 import 和配置引用

**Tech Stack:** Django 4.2, Python

**Spec Reference:** `docs/superpowers/specs/2026-06-11-backend-app-restructure-design.md`

---

## 映射表

### 系统基础 → apps/system/

| 原名 | 新名 | AppConfig.name |
|------|------|----------------|
| app_user | apps/system/app_user | apps.system.app_user |
| app_role | apps/system/app_role | apps.system.app_role |
| app_menu | apps/system/app_menu | apps.system.app_menu |
| app_dept | apps/system/app_dept | apps.system.app_dept |
| app_post | apps/system/app_post | apps.system.app_post |
| app_apis | apps/system/app_apis | apps.system.app_apis |
| app_dict | apps/system/app_dict | apps.system.app_dict |
| app_login | apps/system/app_login | apps.system.app_login |
| app_init | apps/system/app_init | apps.system.app_init |

### 业务模块 → apps/business/

| 原名 | 新名 | AppConfig.name |
|------|------|----------------|
| app_reference | apps/business/app_reference | apps.business.app_reference |
| app_pension_policy | apps/business/app_pension_policy | apps.business.app_pension_policy |
| app_personal_info | apps/business/personnel/app_personal_info | apps.business.personnel.app_personal_info |
| app_personal_died | apps/business/personnel/app_personal_died | apps.business.personnel.app_personal_died |
| app_personal_sacrifice | apps/business/personnel/app_personal_sacrifice | apps.business.personnel.app_personal_sacrifice |
| app_personal_disability | apps/business/personnel/app_personal_disability | apps.business.personnel.app_personal_disability |

### 基础设施 → apps/infrastructure/

| 原名 | 新名 | AppConfig.name |
|------|------|----------------|
| app_crontab | apps/infrastructure/app_crontab | apps.infrastructure.app_crontab |
| app_monitor | apps/infrastructure/app_monitor | apps.infrastructure.app_monitor |
| app_operation_log | apps/infrastructure/app_operation_log | apps.infrastructure.app_operation_log |
| app_message | apps/infrastructure/app_message | apps.infrastructure.app_message |

### 不动

| 原名 | 说明 |
|------|------|
| app_example | 保留在 backend/ 根目录 |
| application | Django 项目配置 |
| utils | 工具模块 |
| static | 静态文件 |
| logs | 日志 |

---

### Task 1: 创建目录结构

**Files:**
- Create: `backend/apps/__init__.py`
- Create: `backend/apps/system/__init__.py`
- Create: `backend/apps/business/__init__.py`
- Create: `backend/apps/business/personnel/__init__.py`
- Create: `backend/apps/infrastructure/__init__.py`

- [ ] **Step 1: 创建所有新目录**

```bash
mkdir -p backend/apps/system
mkdir -p backend/apps/business/personnel
mkdir -p backend/apps/infrastructure
```

- [ ] **Step 2: 创建所有 `__init__.py` 文件**

```bash
touch backend/apps/__init__.py
touch backend/apps/system/__init__.py
touch backend/apps/business/__init__.py
touch backend/apps/business/personnel/__init__.py
touch backend/apps/infrastructure/__init__.py
```

- [ ] **Step 3: 验证目录结构**

```bash
ls -R backend/apps/
```

预期输出:

```
backend/apps/:
business/  infrastructure/  __init__.py  system/

backend/apps/business:
personnel/  __init__.py

backend/apps/business/personnel:
__init__.py

backend/apps/infrastructure:
__init__.py

backend/apps/system:
__init__.py
```

- [ ] **Step 4: 提交**

```bash
git add backend/apps/
git commit -m "feat: create apps/ directory structure for app reorganization

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: 迁移系统基础模块（9 apps → apps/system/）

**Files:**
- Rename: `backend/app_user/` → `backend/apps/system/app_user/`
- Rename: `backend/app_role/` → `backend/apps/system/app_role/`
- Rename: `backend/app_menu/` → `backend/apps/system/app_menu/`
- Rename: `backend/app_dept/` → `backend/apps/system/app_dept/`
- Rename: `backend/app_post/` → `backend/apps/system/app_post/`
- Rename: `backend/app_apis/` → `backend/apps/system/app_apis/`
- Rename: `backend/app_dict/` → `backend/apps/system/app_dict/`
- Rename: `backend/app_login/` → `backend/apps/system/app_login/`
- Rename: `backend/app_init/` → `backend/apps/system/app_init/`

- [ ] **Step 1: 使用 git mv 批量移动**

```bash
cd backend
git mv app_user apps/system/app_user
git mv app_role apps/system/app_role
git mv app_menu apps/system/app_menu
git mv app_dept apps/system/app_dept
git mv app_post apps/system/app_post
git mv app_apis apps/system/app_apis
git mv app_dict apps/system/app_dict
git mv app_login apps/system/app_login
git mv app_init apps/system/app_init
cd ..
```

- [ ] **Step 2: 验证文件已移动**

```bash
ls backend/apps/system/
```

预期: `app_apis/  app_dept/  app_dict/  app_init/  app_login/  app_menu/  app_post/  app_role/  app_user/`

- [ ] **Step 3: 确认原位置已清空**

```bash
ls backend/app_user/ 2>&1
```

预期: `ls: cannot access 'backend/app_user/': No such file or directory`

- [ ] **Step 4: 提交**

```bash
git add -A
git commit -m "refactor: move system apps to apps/system/

- app_user, app_role, app_menu, app_dept, app_post
- app_apis, app_dict, app_login, app_init

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: 迁移基础设模块（4 apps → apps/infrastructure/）

**Files:**
- Rename: `backend/app_crontab/` → `backend/apps/infrastructure/app_crontab/`
- Rename: `backend/app_monitor/` → `backend/apps/infrastructure/app_monitor/`
- Rename: `backend/app_operation_log/` → `backend/apps/infrastructure/app_operation_log/`
- Rename: `backend/app_message/` → `backend/apps/infrastructure/app_message/`

- [ ] **Step 1: 使用 git mv 批量移动**

```bash
cd backend
git mv app_crontab apps/infrastructure/app_crontab
git mv app_monitor apps/infrastructure/app_monitor
git mv app_operation_log apps/infrastructure/app_operation_log
git mv app_message apps/infrastructure/app_message
cd ..
```

- [ ] **Step 2: 验证**

```bash
ls backend/apps/infrastructure/
```

预期: `app_crontab/  app_message/  app_monitor/  app_operation_log/`

- [ ] **Step 3: 提交**

```bash
git add -A
git commit -m "refactor: move infrastructure apps to apps/infrastructure/

- app_crontab, app_monitor, app_operation_log, app_message

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: 迁移业务模块（6 apps → apps/business/）

**Files:**
- Rename: `backend/app_reference/` → `backend/apps/business/app_reference/`
- Rename: `backend/app_pension_policy/` → `backend/apps/business/app_pension_policy/`
- Rename: `backend/app_personal_info/` → `backend/apps/business/personnel/app_personal_info/`
- Rename: `backend/app_personal_died/` → `backend/apps/business/personnel/app_personal_died/`
- Rename: `backend/app_personal_sacrifice/` → `backend/apps/business/personnel/app_personal_sacrifice/`
- Rename: `backend/app_personal_disability/` → `backend/apps/business/personnel/app_personal_disability/`

- [ ] **Step 1: 使用 git mv 批量移动**

```bash
cd backend
git mv app_reference apps/business/app_reference
git mv app_pension_policy apps/business/app_pension_policy
git mv app_personal_info apps/business/personnel/app_personal_info
git mv app_personal_died apps/business/personnel/app_personal_died
git mv app_personal_sacrifice apps/business/personnel/app_personal_sacrifice
git mv app_personal_disability apps/business/personnel/app_personal_disability
cd ..
```

- [ ] **Step 2: 验证目录完整性**

```bash
echo "=== Business ===" && ls backend/apps/business/
echo "=== Personnel ===" && ls backend/apps/business/personnel/
```

预期 business 下: `app_pension_policy/  app_reference/  personnel/`
预期 personnel 下: `app_personal_died/  app_personal_disability/  app_personal_info/  app_personal_sacrifice/`

- [ ] **Step 3: 确认 backend/ 根目录只剩 exmple、application、utils、static、logs、manage.py**

```bash
ls -d backend/app_*/ 2>&1
```

预期只有 `backend/app_example/`

- [ ] **Step 4: 提交**

```bash
git add -A
git commit -m "refactor: move business apps to apps/business/

- app_reference, app_pension_policy → apps/business/
- app_personal_info, app_personal_died, app_personal_sacrifice,
  app_personal_disability → apps/business/personnel/

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: 更新所有 apps.py 文件（19 个）

**Files:**
- Modify: 19 × `apps.py`

- [ ] **Step 1: 更新 apps/system/ 下的 9 个 apps.py**

`backend/apps/system/app_user/apps.py` — 修改 `name`:
```python
from django.apps import AppConfig


class AppUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_user'
```

`backend/apps/system/app_role/apps.py`:
```python
from django.apps import AppConfig


class AppRoleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_role'
```

`backend/apps/system/app_menu/apps.py`:
```python
from django.apps import AppConfig


class AppMenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_menu'
```

`backend/apps/system/app_dept/apps.py`:
```python
from django.apps import AppConfig


class AppDeptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_dept'
```

`backend/apps/system/app_post/apps.py`:
```python
from django.apps import AppConfig


class AppPostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_post'
```

`backend/apps/system/app_apis/apps.py`:
```python
from django.apps import AppConfig


class AppApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_apis'
```

`backend/apps/system/app_dict/apps.py`:
```python
from django.apps import AppConfig


class AppDictConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_dict'
```

`backend/apps/system/app_login/apps.py`:
```python
from django.apps import AppConfig


class AppLoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_login'
```

`backend/apps/system/app_init/apps.py`:
```python
from django.apps import AppConfig


class AppInitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.system.app_init'

    def ready(self):
        import apps.system.app_init.management.commands
```

- [ ] **Step 2: 更新 apps/infrastructure/ 下的 4 个 apps.py**

`backend/apps/infrastructure/app_crontab/apps.py`:
```python
from django.apps import AppConfig


class AppCrontabConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.infrastructure.app_crontab'
```

`backend/apps/infrastructure/app_monitor/apps.py`:
```python
from django.apps import AppConfig


class AppMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.infrastructure.app_monitor'
```

`backend/apps/infrastructure/app_operation_log/apps.py`:
```python
from django.apps import AppConfig


class AppOperationLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.infrastructure.app_operation_log'
```

`backend/apps/infrastructure/app_message/apps.py`:
```python
from django.apps import AppConfig


class AppMessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.infrastructure.app_message'
```

- [ ] **Step 3: 更新 apps/business/ 下的 6 个 apps.py**

`backend/apps/business/app_reference/apps.py`:
```python
from django.apps import AppConfig


class AppReferenceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.business.app_reference"
    verbose_name = "执法管理-案件质量-评查依据"
```

`backend/apps/business/app_pension_policy/apps.py`:
```python
from django.apps import AppConfig


class AppPensionPolicyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.app_pension_policy'
```

`backend/apps/business/personnel/app_personal_info/apps.py`:
```python
from django.apps import AppConfig


class AppPersonalInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.personnel.app_personal_info'
```

`backend/apps/business/personnel/app_personal_died/apps.py`:
```python
from django.apps import AppConfig


class AppPersonalDiedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.personnel.app_personal_died'
```

`backend/apps/business/personnel/app_personal_sacrifice/apps.py`:
```python
from django.apps import AppConfig


class AppPersonalSacrificeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.personnel.app_personal_sacrifice'
```

`backend/apps/business/personnel/app_personal_disability/apps.py`:
```python
from django.apps import AppConfig


class AppPersonalDisabilityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.business.personnel.app_personal_disability'
```

- [ ] **Step 4: 确认 app_example/apps.py 保持不变**

验证文件内容仍为:
```python
from django.apps import AppConfig


class AppExampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_example'
```

- [ ] **Step 5: 提交**

```bash
git add -A
git commit -m "refactor: update AppConfig.name to full dotted paths

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 6: 更新 application/settings.py

**Files:**
- Modify: `backend/application/settings.py`

- [ ] **Step 1: 更新 INSTALLED_APPS 中所有 app_* 条目（第 63-82 行）**

将 settings.py 第 63-82 行替换为:

```python
    'apps.system.app_post',  # 系统-岗位
    'apps.system.app_dept',  # 系统-部门
    'apps.system.app_menu',  # 系统-菜单
    'apps.system.app_apis',  # 系统-API
    'apps.system.app_role',  # 系统-角色
    'apps.system.app_user',  # 系统-用户
    'apps.system.app_login',  # 系统-登录
    'apps.system.app_dict',  # 系统-字典
    'apps.infrastructure.app_crontab',  # celery定时任务
    'apps.infrastructure.app_monitor',  # 任务监控
    'apps.infrastructure.app_operation_log',  # 操作日志
    'apps.infrastructure.app_message',  # 信息中心
    'app_example',  # 测试样例
    'apps.system.app_init',  # 数据初始化
    'apps.business.app_reference',  # 执法管理-案件质量-评查依据
    'apps.business.personnel.app_personal_info',  # 优抚一件事-人员管理-基本信息
    'apps.business.personnel.app_personal_died',  # 优抚一件事-人员管理-病故人员
    'apps.business.personnel.app_personal_sacrifice',  # 优抚一件事-人员管理-因公牺牲人员
    'apps.business.personnel.app_personal_disability',  # 优抚一件事-人员管理-伤残人员
```

- [ ] **Step 2: 更新 AUTH_USER_MODEL（第 151 行）**

```python
AUTH_USER_MODEL = "apps.system.app_user.Users"
```

- [ ] **Step 3: 提交**

```bash
git add backend/application/settings.py
git commit -m "refactor: update settings.py INSTALLED_APPS and AUTH_USER_MODEL

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 7: 更新 application/urls.py

**Files:**
- Modify: `backend/application/urls.py`

- [ ] **Step 1: 更新第 20 行 import**

```python
from apps.system.app_login.views import CaptchaView, LoginView
```

- [ ] **Step 2: 更新所有 include() 路径（第 26-43 行）**

```python
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
```

- [ ] **Step 3: 提交**

```bash
git add backend/application/urls.py
git commit -m "refactor: update urls.py includes to new app paths

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 8: 更新跨 app import 语句（所有 Python 文件）

**Files:** 约 30+ 个文件

- [ ] **Step 1: 更新 application/websocketConfig.py（第 18 行）**

```python
from apps.infrastructure.app_message.models import MessageCenterTargetUser, MessageCenter
```

- [ ] **Step 2: 更新 utils/serializers.py（第 13 行）**

```python
from apps.system.app_user.models import Users
```

- [ ] **Step 3: 更新 utils/permission.py（第 23 行）**

```python
                from apps.system.app_apis.models import APIS
```

- [ ] **Step 4: 更新 apps/system/app_login/serializer.py（第 17 行）**

```python
from apps.system.app_user.models import Users
```

其余内部 import（`from .models import` 风格）不需要改，因为它们使用相对引用。

- [ ] **Step 5: 更新 apps/system/app_user/ 的 imports**

`backend/apps/system/app_user/views.py`:
```python
from apps.system.app_menu.models import Menu
from apps.system.app_menu.serializer import MenuSerializer
from apps.system.app_user.models import Users
from apps.system.app_user.serializers import UserSerializer, UserCreateSerializer, UserInfoUpdateSerializer, UserResource
```

`backend/apps/system/app_user/serializers.py`:
```python
from apps.system.app_post.models import Post
from apps.system.app_role.models import Role
from apps.system.app_dept.models import Dept
from apps.system.app_user.models import Users
```

`backend/apps/system/app_user/urls.py`:
```python
from apps.system.app_user.views import UserViewSet
```

- [ ] **Step 6: 更新 apps/system/app_role/ 的 imports**

`backend/apps/system/app_role/serializers.py`:
```python
from apps.system.app_dept.models import Dept
from apps.system.app_menu.models import Menu
from apps.system.app_role.models import Role
```

`backend/apps/system/app_role/urls.py`:
```python
from apps.system.app_role.views import RoleViewSet
```

- [ ] **Step 7: 更新 apps/system/app_dept/ 的 imports**

`backend/apps/system/app_dept/views.py`:
```python
from apps.system.app_dept.models import Dept
from apps.system.app_dept.serializers import DeptSerializer, DeptTreeSerializer, DeptCreateUpdateSerializer
```

`backend/apps/system/app_dept/serializers.py`:
```python
from apps.system.app_dept.models import Dept
```

`backend/apps/system/app_dept/urls.py`:
```python
from apps.system.app_dept.views import DeptViewSet
```

- [ ] **Step 8: 更新 apps/system/app_menu/ 的 imports**

`backend/apps/system/app_menu/views.py`:
```python
from apps.system.app_menu.models import Menu
from apps.system.app_menu.serializer import MenuSerializer, MenuTreeSerializer
```

`backend/apps/system/app_menu/serializer.py`:
```python
from apps.system.app_menu.models import Menu
```

`backend/apps/system/app_menu/urls.py`:
```python
from apps.system.app_menu.views import MenuViewSet
```

- [ ] **Step 9: 更新 apps/system/app_dict/ 的 imports**

`backend/apps/system/app_dict/views.py`:
```python
from apps.system.app_dict.models import DictType, DictData
from apps.system.app_dict.serializers import DictTypeSerializer, DictDataSerializer, DictTypeCreateSerializer
```

`backend/apps/system/app_dict/serializers.py`:
```python
from apps.system.app_dict.models import DictData, DictType
```

`backend/apps/system/app_dict/urls.py`:
```python
from apps.system.app_dict.views import DictDataViewSet, DictTypeViewSet
```

- [ ] **Step 10: 更新 apps/system/app_apis/ 的 imports**

`backend/apps/system/app_apis/views.py`:
```python
from apps.system.app_apis.models import APIS
from apps.system.app_apis.serializers import ApiSerializer
```

`backend/apps/system/app_apis/serializers.py`:
```python
from apps.system.app_apis.models import APIS
```

`backend/apps/system/app_apis/urls.py`:
```python
from apps.system.app_apis.views import ApisViewSet
```

- [ ] **Step 11: 更新 apps/infrastructure/app_message/ 的 imports**

`backend/apps/infrastructure/app_message/models.py`:
```python
from apps.system.app_dept.models import Dept
from apps.system.app_role.models import Role
from apps.system.app_user.models import Users
```

`backend/apps/infrastructure/app_message/views.py`:
```python
from apps.infrastructure.app_message.models import MessageCenter, MessageCenterTargetUser
from apps.infrastructure.app_message.serializer import MessageCenterSerializer, MessageCenterCreateSerializer, MessageCenterTargetUserListSerializer
```

`backend/apps/infrastructure/app_message/serializer.py`:
```python
from apps.infrastructure.app_message.models import MessageCenter
from apps.infrastructure.app_message.models import MessageCenterTargetUser
from apps.system.app_user.models import Users
```
以及第 30 行的 lazy import:
```python
        from apps.system.app_role.serializers import RoleSerializer
```
第 42 行:
```python
        from apps.system.app_user.serializers import UserSerializer
```
第 54 行:
```python
        from apps.system.app_dept.serializers import DeptSerializer
```

`backend/apps/infrastructure/app_message/urls.py`:
```python
from apps.infrastructure.app_message.views import MessageCenterViewSet
```

- [ ] **Step 12: 更新 apps/infrastructure/app_crontab/ 的 imports**

`backend/apps/infrastructure/app_crontab/urls.py`:
```python
from apps.infrastructure.app_crontab.views.celery_clocked_schedule import ClockedScheduleModelViewSet
from apps.infrastructure.app_crontab.views.celery_interval_schedule import IntervalScheduleModelViewSet
from apps.infrastructure.app_crontab.views.celery_crontab_schedule import CrontabScheduleModelViewSet
from apps.infrastructure.app_crontab.views.celery_periodic_task import PeriodicTaskModelViewSet
from apps.infrastructure.app_crontab.views.celery_task_result import CeleryTaskResultViewSet
```

`backend/apps/infrastructure/app_crontab/views/celery_periodic_task.py`:
```python
from apps.infrastructure.app_crontab.filters import CeleryPeriodicTaskFilterSet
from apps.infrastructure.app_crontab.views.celery_crontab_schedule import CrontabScheduleSerializer
from apps.infrastructure.app_crontab.views.celery_interval_schedule import IntervalScheduleSerializer
```

`backend/apps/infrastructure/app_crontab/views/celery_task_result.py`:
```python
from apps.infrastructure.app_crontab.filters import CeleryTaskResultFilterSet
```

- [ ] **Step 13: 更新 apps/infrastructure/app_monitor/ 的 imports**

`backend/apps/infrastructure/app_monitor/views.py`:
```python
from apps.infrastructure.app_monitor.models import MonitorManage
from apps.infrastructure.app_monitor.serializer import MonitorManageSerializer
```

`backend/apps/infrastructure/app_monitor/serializer.py`:
```python
from apps.infrastructure.app_monitor.models import MonitorManage
```

`backend/apps/infrastructure/app_monitor/urls.py`:
```python
from apps.infrastructure.app_monitor.views import MonitorManageViewSet
```

- [ ] **Step 14: 更新 apps/infrastructure/app_operation_log/ 的 imports**

`backend/apps/infrastructure/app_operation_log/views.py`:
```python
from apps.infrastructure.app_operation_log.filters import OperationLogTimeFilter
from apps.infrastructure.app_operation_log.models import OperationLog
from apps.infrastructure.app_operation_log.serializers import OperationLogSerializer
```

`backend/apps/infrastructure/app_operation_log/serializers.py`:
```python
from apps.infrastructure.app_operation_log.models import OperationLog
```

`backend/apps/infrastructure/app_operation_log/filters.py`:
```python
from apps.infrastructure.app_operation_log.models import OperationLog
```

`backend/apps/infrastructure/app_operation_log/urls.py`:
```python
from apps.infrastructure.app_operation_log.views import OperationLogViewSet
```

- [ ] **Step 15: 更新 apps/business/personnel/ 的 imports**

`backend/apps/business/personnel/app_personal_info/views.py`:
```python
from apps.business.personnel.app_personal_info.filters import PersonalInfoFilter
from apps.business.personnel.app_personal_info.models import PersonalInfo
```

`backend/apps/business/personnel/app_personal_info/admin.py`:
```python
from apps.business.personnel.app_personal_info.models import PersonalInfo
```

`backend/apps/business/personnel/app_personal_died/views.py`:
```python
from apps.business.personnel.app_personal_info.models import PersonalInfo
from apps.business.personnel.app_personal_info.serializers import PersonalInfoSerializer
from apps.business.personnel.app_personal_died.filters import PersonalDiedFilter
from apps.business.personnel.app_personal_died.models import PersonalDied
from apps.business.personnel.app_personal_died.serializers import (
    PersonalDiedSerializer,
    PersonalDiedCreateSerializer,
    PersonalDiedUpdateSerializer,
)
```

`backend/apps/business/personnel/app_personal_died/serializers.py`:
```python
from apps.business.personnel.app_personal_info.models import PersonalInfo
from apps.business.personnel.app_personal_died.models import PersonalDied
```

`backend/apps/business/personnel/app_personal_died/admin.py`:
```python
from apps.business.personnel.app_personal_info.models import PersonalInfo
```

`backend/apps/business/personnel/app_personal_died/urls.py`:
```python
from apps.business.personnel.app_personal_died.views import PersonalDiedViewSet
```

`backend/apps/business/personnel/app_personal_died/filters.py`:
```python
from apps.business.personnel.app_personal_died.models import PersonalDied
```

`backend/apps/business/personnel/app_personal_sacrifice/views.py`:
```python
from apps.business.personnel.app_personal_info.models import PersonalInfo
from apps.business.personnel.app_personal_info.serializers import PersonalInfoSerializer
from apps.business.personnel.app_personal_sacrifice.filters import PersonalSacrificeFilter
from apps.business.personnel.app_personal_sacrifice.models import PersonalSacrifice
from apps.business.personnel.app_personal_sacrifice.serializers import (
    PersonalSacrificeSerializer,
    PersonalSacrificeCreateSerializer,
    PersonalSacrificeUpdateSerializer,
)
```

`backend/apps/business/personnel/app_personal_sacrifice/serializers.py`:
```python
from apps.business.personnel.app_personal_info.models import PersonalInfo
from apps.business.personnel.app_personal_sacrifice.models import PersonalSacrifice
```

`backend/apps/business/personnel/app_personal_sacrifice/urls.py`:
```python
from apps.business.personnel.app_personal_sacrifice.views import PersonalSacrificeViewSet
```

`backend/apps/business/personnel/app_personal_sacrifice/filters.py`:
```python
from apps.business.personnel.app_personal_sacrifice.models import PersonalSacrifice
```

- [ ] **Step 16: 更新 apps/business/ 的 imports**

`backend/apps/business/app_reference/views.py`:
```python
from apps.business.app_reference.models import ReviewBasis
from apps.business.app_reference.serializers import (
    ReviewBasisSerializer,
    ReviewBasisCreateSerializer,
    ReviewBasisUpdateSerializer,
)
```

`backend/apps/business/app_reference/serializers.py`:
```python
from apps.business.app_reference.models import ReviewBasis
```

`backend/apps/business/app_reference/urls.py`:
```python
from apps.business.app_reference.views import ReviewBasisViewSet
```

- [ ] **Step 17: 更新 app_example imports**

`backend/app_example/views.py`:
```python
from app_example.models import Example
from app_example.serializers import ExampleSerializer, ExampleCreateUpdateSerializer
```

`backend/app_example/serializers.py`:
```python
from app_example.models import Example
```

`backend/app_example/urls.py`:
```python
from app_example.views import ExampleViewSet
```

`backend/app_example/admin.py`:
```python
from app_example.models import Example
```

- [ ] **Step 18: 提交**

```bash
git add -A
git commit -m "refactor: update all cross-app imports to new paths

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 9: 验证 — Django 系统检查

**Files:** 无需修改

- [ ] **Step 1: 运行 Django 系统检查**

```bash
cd backend && python manage.py check
```

预期: `System check identified no issues (0 silenced).`

- [ ] **Step 2: 运行 makemigrations 干跑（确认无新迁移产生）**

```bash
cd backend && python manage.py makemigrations --dry-run
```

预期: `No changes detected`

- [ ] **Step 3: 如果以上任一步骤报错，检查错误信息并修复**

常见错误及修复:
- `ImportError: No module named 'app_xxx'` → 检查对应文件的 import 是否已更新
- `ModuleNotFoundError` → 检查 `__init__.py` 是否存在
- `django.core.exceptions.ImproperlyConfigured` → 检查 `AppConfig.name` 和 `INSTALLED_APPS` 路径是否匹配

---

### Task 10: 最终提交并清理

- [ ] **Step 1: 确认所有改动已提交**

```bash
git status
```

预期: `nothing to commit, working tree clean`

- [ ] **Step 2: 查看最终目录结构**

```bash
ls -R backend/apps/ --format=single-column | head -60
```

- [ ] **Step 3: 确认 backend/ 根目录整洁**

```bash
ls backend/
```

预期仅看到: `app_example/  application/  apps/  logs/  manage.py  model.conf  requirements.txt  static/  utils/`

---
