# Backend App 目录重构设计文档

**日期**: 2026-06-11
**状态**: Approved

## 1. 背景与目标

当前 `backend/` 下有 20 个 `app_*` 前缀的 Django app 平铺在根目录，随着业务增长变得难以导航和维护。目标是将它们按业务域分组到子目录中，同时**不影响系统正常运行**。

## 2. 目标结构

```
backend/
├── apps/
│   ├── __init__.py                          # 新建
│   │
│   ├── system/                              # 系统基础模块
│   │   ├── __init__.py                      # 新建
│   │   ├── app_user/                        # 用户管理
│   │   ├── app_role/                        # 角色管理
│   │   ├── app_menu/                        # 菜单管理
│   │   ├── app_dept/                        # 部门管理
│   │   ├── app_post/                        # 岗位管理
│   │   ├── app_apis/                        # API权限管理
│   │   ├── app_dict/                        # 数据字典
│   │   ├── app_login/                       # 登录认证
│   │   └── app_init/                        # 数据初始化
│   │
│   ├── business/                            # 业务模块
│   │   ├── __init__.py                      # 新建
│   │   ├── personnel/
│   │   │   ├── __init__.py                  # 新建
│   │   │   ├── app_personal_info/           # 优抚-基本信息
│   │   │   ├── app_personal_died/           # 优抚-病故人员
│   │   │   ├── app_personal_sacrifice/      # 优抚-因公牺牲人员
│   │   │   └── app_personal_disability/     # 优抚-伤残人员
│   │   ├── app_pension_policy/              # 优抚-政策管理
│   │   └── app_reference/                   # 执法管理-评查依据
│   │
│   └── infrastructure/                      # 基础设施模块
│       ├── __init__.py                      # 新建
│       ├── app_crontab/                     # Celery定时任务
│       ├── app_monitor/                     # 任务监控
│       ├── app_operation_log/               # 操作日志
│       └── app_message/                     # 消息中心
│
├── app_example/          # 测试样例，保留在根目录，不移入 apps/
├── application/          # Django项目配置，不变
├── utils/                # 工具模块，不变
├── static/               # 静态文件，不变
├── logs/                 # 日志，不变
└── manage.py             # 入口，不变
```

## 3. 分组依据

| 分组 | 包含 App | 依据 |
|------|----------|------|
| `apps/system/` | user, role, menu, dept, post, apis, dict, login, init | 系统基础功能，被其他模块依赖 |
| `apps/business/personnel/` | personal_info, personal_died, personal_sacrifice, personal_disability | 优抚一件事-人员管理子域，后三者共享 personal_info |
| `apps/business/` | pension_policy, reference | 独立业务模块，无内部依赖 |
| `apps/infrastructure/` | crontab, monitor, operation_log, message | 基础设施/运维支持 |
| `app_example/` | （保留在根目录） | 测试样例，非生产代码 |

## 4. 技术实现方案

### 4.1 AppConfig.name 变更

每个 app 的 `apps.py` 中 `AppConfig.name` 从短名改为完整 Python 路径：

```python
# 改前
class AppUserConfig(AppConfig):
    name = 'app_user'

# 改后
class AppUserConfig(AppConfig):
    name = 'apps.system.app_user'
```

**关键原理：** Django 的 `AppConfig.label` 默认取 `name` 的最后一段。所以即使 `name` 变成 `apps.system.app_user`，`label` 仍然是 `app_user`。数据库表名、迁移文件中的外键引用都使用 `label`，因此**不需要修改迁移文件和数据库**。

### 4.2 需要修改的文件清单

| 文件/类别 | 修改内容 | 数量 |
|-----------|----------|------|
| `*/apps.py` | 修改 `name` 为完整路径 | 19 个 |
| `application/settings.py` | 更新 `INSTALLED_APPS` 和 `AUTH_USER_MODEL` | ~22 行 |
| `application/urls.py` | 更新 `include()` 路径 | ~15 行 |
| `application/websocketConfig.py` | 更新 import 路径 | ~2 处 |
| 各 app 的 `*.py` | 更新 `from app_xxx import` 为 `from apps.xxx.app_xxx import` | ~60+ 处 |
| 各 app 的 `migrations/*.py` | **不需要改** | 0 |
| 新建 `__init__.py` | `apps/`, `apps/system/`, `apps/business/`, `apps/business/personnel/`, `apps/infrastructure/` | 5 个 |

### 4.3 settings.py 变更示例

```python
INSTALLED_APPS = [
    # ... 第三方 app 不变 ...
    'apps.system.app_post',
    'apps.system.app_dept',
    'apps.system.app_menu',
    'apps.system.app_apis',
    'apps.system.app_role',
    'apps.system.app_user',
    'apps.system.app_login',
    'apps.system.app_dict',
    'apps.system.app_init',
    'apps.infrastructure.app_crontab',
    'apps.infrastructure.app_monitor',
    'apps.infrastructure.app_operation_log',
    'apps.infrastructure.app_message',
    'app_example',                    # 保留原名
    'apps.business.app_reference',
    'apps.business.app_pension_policy',
    'apps.business.personnel.app_personal_info',
    'apps.business.personnel.app_personal_died',
    'apps.business.personnel.app_personal_sacrifice',
    'apps.business.personnel.app_personal_disability',
]

AUTH_USER_MODEL = "apps.system.app_user.Users"
```

### 4.4 跨 app 引用变更示例

```python
# app_message/models.py 改前
from app_user.models import Users
from app_role.models import Role
from app_dept.models import Dept

# 改后
from apps.system.app_user.models import Users
from apps.system.app_role.models import Role
from apps.system.app_dept.models import Dept
```

## 5. 执行步骤

1. `git checkout -b refactor/backend-app-restructure`
2. 创建新的目录结构 `apps/system/`, `apps/business/personnel/`, `apps/infrastructure/`
3. 使用 `git mv` 将各 app 移动到目标目录（保留 git 历史）
4. 在所有新目录中创建 `__init__.py`
5. 批量更新：
   - 19 个 `apps.py` 中的 `name`
   - `settings.py` 中的 `INSTALLED_APPS` 和 `AUTH_USER_MODEL`
   - `urls.py` 中的 `include()` 路径
   - 所有 `from app_xxx` import 语句
   - `websocketConfig.py` 中的 import
6. 运行 `python manage.py check` 验证 Django 配置
7. 运行 `python manage.py makemigrations --dry-run` 确认无新迁移产生
8. 运行测试（如有）
9. 提交

## 6. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Python import 遗漏 | 运行时 ImportError | 全局搜索替换 + `manage.py check` |
| app_label 误变 | 数据库表找不到 | AppConfig.name 改全路径但保持末段不变 |
| 迁移产生新表 | 数据库不一致 | `makemigrations --dry-run` 验证为 "No changes detected" |
| 前端 API 路径 | 前端调用失败 | 不影响，只改后端 Python 路径 |
| INSTALLED_APPS 顺序 | 依赖初始化顺序 | 保持原有先后顺序不变 |

## 7. 验收标准

- [ ] `python manage.py check` 无错误
- [ ] `python manage.py makemigrations --dry-run` 显示 "No changes detected"
- [ ] 所有 `from app_xxx` 不再存在于代码中（内部自引用除外）
- [ ] `git status` 显示所有文件已正确移动
- [ ] 系统能正常启动
