from django.db import models

from utils.models import BaseModel


class PersonalSacrifice(BaseModel):
    """
    优抚一件事-人员管理-因公牺牲人员（1对1扩展自基本信息）
    """
    IS_MARTYR_CHOICES = (
        ("0", "否"),
        ("1", "是"),
    )

    info = models.OneToOneField(
        'app_personal_info.PersonalInfo',
        on_delete=models.CASCADE,
        related_name='sacrifice_record',
        verbose_name="基本信息",
        help_text="关联的基本信息记录"
    )
    sacrifice_time = models.DateField(verbose_name="牺牲时间", null=True, blank=True, help_text="牺牲时间")
    sacrifice_reason = models.TextField(verbose_name="牺牲原因", null=True, blank=True, help_text="牺牲原因")
    confirmed_sacrifice_time = models.DateField(verbose_name="认定因公牺牲时间", null=True, blank=True, help_text="认定因公牺牲时间")
    martyr_approval_time = models.DateField(verbose_name="批烈时间", null=True, blank=True, help_text="批烈时间")
    is_martyr = models.CharField(max_length=1, default='0', verbose_name="是否烈士", null=True, blank=True, choices=IS_MARTYR_CHOICES, help_text="是否烈士")
    approval_document_number = models.CharField(max_length=200, verbose_name="认定文号", null=True, blank=True, help_text="认定文号")
    enjoy_hero_model_benefits = models.CharField(max_length=200, verbose_name="享受英模或劳模待遇", null=True, blank=True, help_text="享受英模或劳模待遇")

    class Meta:
        db_table = "pension_personal_sacrifice"
        verbose_name = "优抚一件事-人员管理-因公牺牲人员"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.info.name if self.info_id else ""
