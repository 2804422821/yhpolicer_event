"""
优抚一件事-人员管理-病故人员序列化器 - 1对1扩展，扁平化展示
"""
from import_export import resources
from import_export.fields import Field

from app_personal_info.models import PersonalInfo
from app_personal_died.models import PersonalDied
from utils.serializers import CustomModelSerializer
from rest_framework import serializers


# PersonalInfo 中需要扁平化的字段列表
PERSONAL_INFO_FIELDS = [
    "policer_number", "name", "gender", "id_card", "birth_date",
    "nation", "pension_type", "identity_type", "job_level", "dept_name",
    "work_date", "political_status", "brief_achievements",
]


class PersonalDiedSerializer(CustomModelSerializer):
    """
    病故人员 扁平化序列化器（合并基本信息字段 + 病故特有字段）
    """
    # PersonalInfo 扁平字段（source 指向关联对象）
    policer_number = serializers.CharField(source='info.policer_number', max_length=100, required=False, allow_blank=True, allow_null=True, label="警号")
    name = serializers.CharField(source='info.name', max_length=100, required=True, allow_blank=False, label="姓名")
    gender = serializers.CharField(source='info.gender', max_length=1, required=False, allow_blank=True, default="0", label="性别")
    id_card = serializers.CharField(source='info.id_card', max_length=100, required=True, allow_blank=False, label="身份证号")
    birth_date = serializers.DateField(source='info.birth_date', required=False, allow_null=True, label="出生日期")
    nation = serializers.CharField(source='info.nation', max_length=100, required=False, allow_blank=True, allow_null=True, label="民族")
    pension_type = serializers.CharField(source='info.pension_type', max_length=5, required=False, allow_blank=True, default="1", label="抚恤类别")
    identity_type = serializers.CharField(source='info.identity_type', max_length=2, required=False, allow_blank=True, default="0", label="身份")
    job_level = serializers.CharField(source='info.job_level', max_length=100, required=False, allow_blank=True, allow_null=True, label="职务职级")
    dept_name = serializers.CharField(source='info.dept_name', max_length=100, required=False, allow_blank=True, allow_null=True, label="单位名称")
    work_date = serializers.DateField(source='info.work_date', required=False, allow_null=True, label="参公时间")
    political_status = serializers.CharField(source='info.political_status', max_length=5, required=False, allow_blank=True, default="0", label="政治面貌")
    brief_achievements = serializers.CharField(source='info.brief_achievements', required=False, allow_blank=True, allow_null=True, label="简要事迹")

    # PersonalDied 自身字段
    died_reason = serializers.CharField(required=False, allow_blank=True, allow_null=True, label="病故原因")
    policy_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True, label="对应政策")

    class Meta:
        model = PersonalDied
        fields = [
            "id", "info_id",
            "policer_number", "name", "gender", "id_card", "birth_date",
            "nation", "pension_type", "identity_type", "job_level", "dept_name",
            "work_date", "political_status", "brief_achievements",
            "died_reason", "policy_name",
            "creator", "modifier", "creator_name", "modifier_name",
            "create_datetime", "update_datetime",
        ]
        read_only_fields = ["id", "creator", "create_datetime", "update_datetime"]

    def _split_info_data(self, validated_data):
        """从 validated_data 中分离出 PersonalInfo 的扁平字段"""
        info_data = {}
        for field in PERSONAL_INFO_FIELDS:
            if field in validated_data:
                info_data[field] = validated_data.pop(field)
        return info_data

    def _set_info_attrs(self, info, info_data):
        """将扁平字段值写入 PersonalInfo 实例"""
        for field, value in info_data.items():
            setattr(info, field, value)

    def create(self, validated_data):
        info_id = validated_data.pop("info_id", None) or self.initial_data.get("info_id")
        info_data = self._split_info_data(validated_data)

        if info_id:
            info = PersonalInfo.objects.get(id=info_id)
        else:
            info = PersonalInfo.objects.create(**info_data)

        validated_data["info"] = info

        if self.request and str(self.request.user) != "AnonymousUser":
            validated_data["creator"] = self.request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 修改：仅更新 病故原因 和 对应政策，不修改基本信息
        validated_data.pop("info_id", None)
        self._split_info_data(validated_data)  # 丢弃基本信息字段
        return super().update(instance, validated_data)


class PersonalDiedCreateSerializer(PersonalDiedSerializer):
    pass


class PersonalDiedUpdateSerializer(PersonalDiedSerializer):
    class Meta(PersonalDiedSerializer.Meta):
        read_only_fields = PersonalDiedSerializer.Meta.read_only_fields + ["info_id"]


class PersonalDiedResource(resources.ModelResource):
    """
    病故人员 导入/导出 Resource
    列顺序：警号、姓名、身份证号、性别、抚恤类别、民族、出生年月、
            单位名称、身份、职务职级、政治面貌、参公时间、简要事迹、
            病故原因、对应政策、备注
    """
    policer_number = Field(attribute="info__policer_number", column_name="警号")
    name = Field(attribute="info__name", column_name="姓名")
    id_card = Field(attribute="info__id_card", column_name="身份证号")
    gender = Field(attribute="info__gender", column_name="性别")
    pension_type = Field(attribute="info__pension_type", column_name="抚恤类别")
    nation = Field(attribute="info__nation", column_name="民族")
    birth_date = Field(attribute="info__birth_date", column_name="出生年月")
    dept_name = Field(attribute="info__dept_name", column_name="单位名称")
    identity_type = Field(attribute="info__identity_type", column_name="身份")
    job_level = Field(attribute="info__job_level", column_name="职务职级")
    political_status = Field(attribute="info__political_status", column_name="政治面貌")
    work_date = Field(attribute="info__work_date", column_name="参公时间")
    brief_achievements = Field(attribute="info__brief_achievements", column_name="简要事迹")
    died_reason = Field(attribute="died_reason", column_name="病故原因")
    policy_name = Field(attribute="policy_name", column_name="对应政策")

    class Meta:
        model = PersonalDied
        fields = (
            "policer_number", "name", "id_card", "gender", "pension_type", "nation",
            "birth_date", "dept_name", "identity_type", "job_level", "political_status",
            "work_date", "brief_achievements", "died_reason", "policy_name",
        )
        export_order = fields
        import_id_fields = []
        skip_unchanged = True

    def before_import_row(self, row, **kwargs):
        """导入时：先根据身份证号查找或创建 PersonalInfo，再关联 PersonalDied"""
        id_card = row.get("身份证号")
        if id_card:
            info, _ = PersonalInfo.objects.get_or_create(
                id_card=id_card,
                defaults={
                    "name": row.get("姓名", ""),
                    "gender": row.get("性别", "0"),
                    "pension_type": row.get("抚恤类别", "1"),
                    "nation": row.get("民族", ""),
                    "birth_date": row.get("出生年月") or None,
                    "dept_name": row.get("单位名称", ""),
                    "identity_type": row.get("身份", "0"),
                    "job_level": row.get("职务职级", ""),
                    "political_status": row.get("政治面貌", "0"),
                    "work_date": row.get("参公时间") or None,
                    "brief_achievements": row.get("简要事迹", ""),
                    "policer_number": row.get("警号", ""),
                }
            )
            # 检查是否已有 died_record
            if not PersonalDied.objects.filter(info=info).exists():
                PersonalDied.objects.create(info=info)
        return row
