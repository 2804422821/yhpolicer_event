"""
评查依据模块序列化器
"""
from import_export import resources
from import_export.fields import Field

from app_reference.models import ReviewBasis
from utils.serializers import CustomModelSerializer


class ReviewBasisSerializer(CustomModelSerializer):
    """
    评查依据-序列化器
    """

    class Meta:
        model = ReviewBasis
        fields = "__all__"


class ReviewBasisCreateUpdateSerializer(CustomModelSerializer):
    """
    评查依据 创建/更新序列化器
    """

    class Meta:
        model = ReviewBasis
        fields = "__all__"
        read_only_fields = ["id", "creator", "create_datetime", "update_datetime"]


class ReviewBasisResource(resources.ModelResource):
    """
    评查依据 导入/导出 Resource (django-import-export)
    """
    quality_type = Field(attribute='quality_type', column_name='质量标准')
    score_type = Field(attribute='score_type', column_name='记分类型')
    score_content = Field(attribute='score_content', column_name='记分内容')
    deduct_score = Field(attribute='deduct_score', column_name='扣分值')

    class Meta:
        model = ReviewBasis
        fields = ('quality_type', 'score_type', 'score_content', 'deduct_score')
        export_order = fields
        import_id_fields = []
        skip_unchanged = True

