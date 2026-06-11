"""
优抚一件事-人员管理-伤残人员 筛选
"""
import django_filters

from app_personal_disability.models import PersonalDisability


class PersonalDisabilityFilter(django_filters.FilterSet):
    policer_number = django_filters.CharFilter(field_name="info__policer_number", lookup_expr="icontains", label="警号")
    name = django_filters.CharFilter(field_name="info__name", lookup_expr="icontains", label="姓名")
    dept_name = django_filters.CharFilter(field_name="info__dept_name", lookup_expr="icontains", label="单位名称")
    identity_type = django_filters.CharFilter(field_name="info__identity_type", lookup_expr="exact", label="身份")
    pension_type = django_filters.CharFilter(field_name="info__pension_type", lookup_expr="exact", label="抚恤类别")

    class Meta:
        model = PersonalDisability
        fields = ["policer_number", "name", "identity_type", "dept_name", "pension_type"]
