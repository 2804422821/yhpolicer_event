"""
优抚一件事-人员管理-基本信息序列化器 - 基础增删改查、导入导出
"""
from import_export import resources
from import_export.fields import Field

from app_personal_info.models import PersonalInfo
from utils.serializers import CustomModelSerializer


class PersonalInfoSerializer(CustomModelSerializer):
    """
    优抚一件事-人员管理-基本信息 序列化器
    """
    class Meta:
        model = PersonalInfo
        fields = "__all__"
        read_only_fields = ['id'] 

class PersonalInfoCreateSerializer(CustomModelSerializer):
    """
    优抚一件事-人员管理-基本信息 创建序列化器
    """
    class Meta:
        model = PersonalInfo
        fields = "__all__"
        read_only_fields = ['id']

class PersonalInfoUpdateSerializer(CustomModelSerializer):
    """
    优抚一件事-人员管理-基本信息 更新序列化器
    """
    class Meta:
        model = PersonalInfo
        fields = "__all__"
        read_only_fields = ["id", "creator", "create_datetime", "update_datetime"]


class PersonalInfoResource(resources.ModelResource):
    """
    优抚人员基本信息 导入/导出 Resource (django-import-export)
    列顺序：警号、姓名、身份证号、性别、抚恤类别、民族、出生年月、单位名称、身份、职务职级、政治面貌、参公时间、简要事迹、对应政策、备注
    """
    policer_number = Field(attribute="policer_number", column_name="警号")
    name = Field(attribute="name", column_name="姓名")
    id_card = Field(attribute="id_card", column_name="身份证号")
    gender = Field(attribute="gender", column_name="性别")
    pension_type = Field(attribute="pension_type", column_name="抚恤类别")
    nation = Field(attribute="nation", column_name="民族")
    birth_date = Field(attribute="birth_date", column_name="出生年月")
    dept_name = Field(attribute="dept_name", column_name="单位名称")
    identity_type = Field(attribute="identity_type", column_name="身份")
    job_level = Field(attribute="job_level", column_name="职务职级")
    political_status = Field(attribute="political_status", column_name="政治面貌")
    work_date = Field(attribute="work_date", column_name="参公时间")
    brief_achievements = Field(attribute="brief_achievements", column_name="简要事迹")
    policy_name = Field(attribute="policy_name", column_name="对应政策")
    remark = Field(attribute="remark", column_name="备注")

    class Meta:
        model = PersonalInfo
        fields = (
            "policer_number", "name", "id_card", "gender", "pension_type", "nation",
            "birth_date", "dept_name", "identity_type", "job_level", "political_status",
            "work_date", "brief_achievements", "policy_name", "remark",
        )
        export_order = fields
        import_id_fields = []
        skip_unchanged = True