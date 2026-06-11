from django.db import models

from utils.models import BaseModel


class PersonalDisability(BaseModel):
    """
    优抚一件事-人员管理-伤残人员（1对1扩展自基本信息）
    """
    IS_WORK_RELATED_CHOICES = (
        ("0", "否"),
        ("1", "是"),
    )

    info = models.OneToOneField(
        'app_personal_info.PersonalInfo',
        on_delete=models.CASCADE,
        related_name='disability_record',
        verbose_name="基本信息",
        help_text="关联的基本信息记录"
    )
    injury_time = models.DateField(verbose_name="受伤时间", null=True, blank=True, help_text="受伤时间")
    assessment_time = models.DateField(verbose_name="评定时间", null=True, blank=True, help_text="评定时间")
    police_disability_assessment_time = models.DateField(verbose_name="人民警察伤残等级评定时间", null=True, blank=True, help_text="人民警察伤残等级评定时间")
    is_work_related_injury = models.CharField(max_length=1, default='0', verbose_name="是否因公受伤", null=True, blank=True, choices=IS_WORK_RELATED_CHOICES, help_text="是否因公受伤")
    disability_level = models.CharField(max_length=50, verbose_name="致残等级", null=True, blank=True, help_text="致残等级")
    police_disability_level = models.CharField(max_length=50, verbose_name="人民警察伤残等级", null=True, blank=True, help_text="人民警察伤残等级")
    disability_reason = models.TextField(verbose_name="伤残原因", null=True, blank=True, help_text="伤残原因")
    police_category = models.CharField(max_length=100, verbose_name="警种分类", null=True, blank=True, help_text="警种分类")
    enjoy_hero_model_benefits = models.CharField(max_length=200, verbose_name="享受英模或劳模待遇", null=True, blank=True, help_text="享受英模或劳模待遇")
    medical_expense_reimbursement = models.TextField(verbose_name="医疗费用报销情况", null=True, blank=True, help_text="医疗费用报销情况")
    brief_description = models.TextField(verbose_name="简要情况", null=True, blank=True, help_text="简要情况")
    family_difficulties = models.TextField(verbose_name="家属存在问题与困难", null=True, blank=True, help_text="家属存在问题与困难")

    class Meta:
        db_table = "pension_personal_disability"
        verbose_name = "优抚一件事-人员管理-伤残人员"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.info.name if self.info_id else ""
