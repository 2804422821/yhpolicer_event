"""
优抚一件事-人员管理-病故人员 筛选
"""
import django_filters

from apps.business.personnel.app_personal_died.models import PersonalDied


class PersonalDiedFilter(django_filters.FilterSet):
    """筛选条件：通过 info 关联查询基本信息字段"""
    policer_number = django_filters.CharFilter(field_name="info__policer_number", lookup_expr="icontains", label="警号")
    name = django_filters.CharFilter(field_name="info__name", lookup_expr="icontains", label="姓名")
    dept_name = django_filters.CharFilter(field_name="info__dept_name", lookup_expr="icontains", label="单位名称")
    identity_type = django_filters.CharFilter(field_name="info__identity_type", lookup_expr="exact", label="身份")
    pension_type = django_filters.CharFilter(field_name="info__pension_type", lookup_expr="exact", label="抚恤类别")

    class Meta:
        model = PersonalDied
        fields = ["policer_number", "name", "identity_type", "dept_name", "pension_type"]
