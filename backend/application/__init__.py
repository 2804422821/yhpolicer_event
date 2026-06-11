# Compatibility: redirect old app module names to new locations
# Required for pickle deserialization of cached data (Redis, Celery results)
# that references the old module paths (e.g. app_apis.models.APIS)
import sys

_APP_REDIRECTS = {
    'app_user': 'apps.system.app_user',
    'app_role': 'apps.system.app_role',
    'app_menu': 'apps.system.app_menu',
    'app_dept': 'apps.system.app_dept',
    'app_post': 'apps.system.app_post',
    'app_apis': 'apps.system.app_apis',
    'app_dict': 'apps.system.app_dict',
    'app_login': 'apps.system.app_login',
    'app_init': 'apps.system.app_init',
    'app_crontab': 'apps.infrastructure.app_crontab',
    'app_monitor': 'apps.infrastructure.app_monitor',
    'app_operation_log': 'apps.infrastructure.app_operation_log',
    'app_message': 'apps.infrastructure.app_message',
    'app_reference': 'apps.business.app_reference',
    'app_pension_policy': 'apps.business.app_pension_policy',
    'app_personal_info': 'apps.business.personnel.app_personal_info',
    'app_personal_died': 'apps.business.personnel.app_personal_died',
    'app_personal_sacrifice': 'apps.business.personnel.app_personal_sacrifice',
    'app_personal_disability': 'apps.business.personnel.app_personal_disability',
}


class _CompatFinder:
    """A meta path finder that redirects old app module names to new locations."""

    def find_module(self, fullname, path=None):
        for old, new in _APP_REDIRECTS.items():
            if fullname == old or fullname.startswith(old + '.'):
                return self
        return None

    def load_module(self, fullname):
        import importlib
        for old, new in _APP_REDIRECTS.items():
            if fullname == old or fullname.startswith(old + '.'):
                # Replace old prefix with new path
                new_name = fullname.replace(old, new, 1)
                mod = importlib.import_module(new_name)
                sys.modules[fullname] = mod
                return mod
        raise ImportError(fullname)


sys.meta_path.insert(0, _CompatFinder())
