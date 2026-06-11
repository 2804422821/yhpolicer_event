"""
优抚一件事-人员管理-基本信息 筛选
"""
import django_filters

from apps.business.personnel.app_personal_info.models import PersonalInfo


class PersonalInfoFilter(django_filters.FilterSet):
    """筛选条件：警号、姓名（模糊）、身份、单位名称（模糊）、抚恤类别（精确）"""
    policer_number = django_filters.CharFilter(lookup_expr="icontains", label="警号")
    name = django_filters.CharFilter(lookup_expr="icontains", label="姓名")
    dept_name = django_filters.CharFilter(lookup_expr="icontains", label="单位名称")

    class Meta:
        model = PersonalInfo
        fields = ["policer_number", "name", "identity_type", "dept_name", "pension_type"]
