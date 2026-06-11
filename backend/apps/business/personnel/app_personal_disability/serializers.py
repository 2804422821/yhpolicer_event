"""
优抚一件事-人员管理-伤残人员序列化器 - 1对1扩展，扁平化展示
"""
from import_export import resources
from import_export.fields import Field

from app_personal_info.models import PersonalInfo
from app_personal_disability.models import PersonalDisability
from utils.serializers import CustomModelSerializer
from rest_framework import serializers


PERSONAL_INFO_FIELDS = [
    "policer_number", "name", "gender", "id_card", "birth_date",
    "nation", "pension_type", "identity_type", "job_level", "dept_name",
    "work_date", "political_status", "brief_achievements",
]


class PersonalDisabilitySerializer(CustomModelSerializer):
    # PersonalInfo 扁平字段（source 指向关联对象）
    policer_number = serializers.CharField(source='info.policer_number', max_length=100, required=False, allow_blank=True, allow_null=True, label="警号")
    name = serializers.CharField(source='info.name', max_length=100, required=True, allow_blank=False, label="姓名")
    gender = serializers.CharField(source='info.gender', max_length=1, required=False, allow_blank=True, default="0", label="性别")
    id_card = serializers.CharField(source='info.id_card', max_length=100, required=True, allow_blank=False, label="身份证号")
    birth_date = serializers.DateField(source='info.birth_date', required=False, allow_null=True, label="出生日期")
    nation = serializers.CharField(source='info.nation', max_length=100, required=False, allow_blank=True, allow_null=True, label="民族")
    pension_type = serializers.CharField(source='info.pension_type', max_length=5, required=False, allow_blank=True, default="2", label="抚恤类别")
    identity_type = serializers.CharField(source='info.identity_type', max_length=2, required=False, allow_blank=True, default="0", label="身份")
    job_level = serializers.CharField(source='info.job_level', max_length=100, required=False, allow_blank=True, allow_null=True, label="职务职级")
    dept_name = serializers.CharField(source='info.dept_name', max_length=100, required=False, allow_blank=True, allow_null=True, label="单位名称")
    work_date = serializers.DateField(source='info.work_date', required=False, allow_null=True, label="参公时间")
    political_status = serializers.CharField(source='info.political_status', max_length=5, required=False, allow_blank=True, default="0", label="政治面貌")
    brief_achievements = serializers.CharField(source='info.brief_achievements', required=False, allow_blank=True, allow_null=True, label="简要事迹")

    # PersonalDisability 自身字段
    injury_time = serializers.DateField(required=False, allow_null=True, label="受伤时间")
    assessment_time = serializers.DateField(required=False, allow_null=True, label="评定时间")
    police_disability_assessment_time = serializers.DateField(required=False, allow_null=True, label="人民警察伤残等级评定时间")
    is_work_related_injury = serializers.CharField(max_length=1, required=False, allow_blank=True, default="0", label="是否因公受伤")
    disability_level = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True, label="致残等级")
    police_disability_level = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True, label="人民警察伤残等级")
    disability_reason = serializers.CharField(required=False, allow_blank=True, allow_null=True, label="伤残原因")
    police_category = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True, label="警种分类")
    enjoy_hero_model_benefits = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True, label="享受英模或劳模待遇")
    medical_expense_reimbursement = serializers.CharField(required=False, allow_blank=True, allow_null=True, label="医疗费用报销情况")
    brief_description = serializers.CharField(required=False, allow_blank=True, allow_null=True, label="简要情况")
    family_difficulties = serializers.CharField(required=False, allow_blank=True, allow_null=True, label="家属存在问题与困难")

    class Meta:
        model = PersonalDisability
        fields = [
            "id", "info_id",
            "policer_number", "name", "gender", "id_card", "birth_date",
            "nation", "pension_type", "identity_type", "job_level", "dept_name",
            "work_date", "political_status", "brief_achievements",
            "injury_time", "assessment_time", "police_disability_assessment_time",
            "is_work_related_injury", "disability_level", "police_disability_level",
            "disability_reason", "police_category", "enjoy_hero_model_benefits",
            "medical_expense_reimbursement", "brief_description", "family_difficulties",
            "creator", "modifier", "creator_name", "modifier_name",
            "create_datetime", "update_datetime",
        ]
        read_only_fields = ["id", "creator", "create_datetime", "update_datetime"]

    def _split_info_data(self, validated_data):
        info_data = {}
        for field in PERSONAL_INFO_FIELDS:
            if field in validated_data:
                info_data[field] = validated_data.pop(field)
        return info_data

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
        validated_data.pop("info_id", None)
        self._split_info_data(validated_data)
        return super().update(instance, validated_data)


class PersonalDisabilityCreateSerializer(PersonalDisabilitySerializer):
    pass


class PersonalDisabilityUpdateSerializer(PersonalDisabilitySerializer):
    class Meta(PersonalDisabilitySerializer.Meta):
        read_only_fields = PersonalDisabilitySerializer.Meta.read_only_fields + ["info_id"]


class PersonalDisabilityResource(resources.ModelResource):
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
    injury_time = Field(attribute="injury_time", column_name="受伤时间")
    assessment_time = Field(attribute="assessment_time", column_name="评定时间")
    police_disability_assessment_time = Field(attribute="police_disability_assessment_time", column_name="人民警察伤残等级评定时间")
    is_work_related_injury = Field(attribute="is_work_related_injury", column_name="是否因公受伤")
    disability_level = Field(attribute="disability_level", column_name="致残等级")
    police_disability_level = Field(attribute="police_disability_level", column_name="人民警察伤残等级")
    disability_reason = Field(attribute="disability_reason", column_name="伤残原因")
    police_category = Field(attribute="police_category", column_name="警种分类")
    enjoy_hero_model_benefits = Field(attribute="enjoy_hero_model_benefits", column_name="享受英模或劳模待遇")
    medical_expense_reimbursement = Field(attribute="medical_expense_reimbursement", column_name="医疗费用报销情况")
    brief_description = Field(attribute="brief_description", column_name="简要情况")
    family_difficulties = Field(attribute="family_difficulties", column_name="家属存在问题与困难")

    class Meta:
        model = PersonalDisability
        fields = (
            "policer_number", "name", "id_card", "gender", "pension_type", "nation",
            "birth_date", "dept_name", "identity_type", "job_level", "political_status",
            "work_date", "brief_achievements", "injury_time", "assessment_time",
            "police_disability_assessment_time", "is_work_related_injury", "disability_level",
            "police_disability_level", "disability_reason", "police_category",
            "enjoy_hero_model_benefits", "medical_expense_reimbursement",
            "brief_description", "family_difficulties",
        )
        export_order = fields
        import_id_fields = []
        skip_unchanged = True

    def before_import_row(self, row, **kwargs):
        id_card = row.get("身份证号")
        if id_card:
            info, _ = PersonalInfo.objects.get_or_create(
                id_card=id_card,
                defaults={
                    "name": row.get("姓名", ""),
                    "gender": row.get("性别", "0"),
                    "pension_type": row.get("抚恤类别", "2"),
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
            if not PersonalDisability.objects.filter(info=info).exists():
                PersonalDisability.objects.create(info=info)
        return row
