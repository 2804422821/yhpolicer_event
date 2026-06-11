from django.db import models

from utils.models import BaseModel, table_prefix


class ReviewBasis(BaseModel):
    """
    执法管理-案件质量-评查依据
    """

    quality_type = models.CharField(
        max_length=100,
        verbose_name="质量标准",
        help_text="质量标准",
    )
    score_type = models.CharField(
        max_length=100,
        verbose_name="记分类型",
        help_text="记分类型",
    )
    score_content = models.TextField(
        verbose_name="记分内容",
        help_text="记分内容",
    )
    deduct_score = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name="扣分值",
        help_text="扣分值",
    )

    class Meta:
        db_table = table_prefix + "enforcement_case_quality_review_basis"
        verbose_name = "执法管理-案件质量-评查依据"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return f"{self.quality_type}-{self.score_type}-{self.score_content[:20]}"

