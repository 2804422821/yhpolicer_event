from django.db import models

from utils.models import BaseModel


class PersonalDied(BaseModel):
    """
    优抚一件事-人员管理-病故人员（1对1扩展自基本信息）
    """
    info = models.OneToOneField(
        'app_personal_info.PersonalInfo',
        on_delete=models.CASCADE,
        related_name='died_record',
        verbose_name="基本信息",
        help_text="关联的基本信息记录"
    )
    died_reason = models.TextField(verbose_name="病故原因", null=True, blank=True, help_text="病故原因")
    policy_name = models.CharField(max_length=100, verbose_name="对应政策", null=True, blank=True, help_text="对应政策")

    class Meta:
        db_table = "pension_personal_died"
        verbose_name = "优抚一件事-人员管理-病故人员"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.info.name if self.info_id else ""
