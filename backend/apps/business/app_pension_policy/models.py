from django.db import models

from utils.models import BaseModel


class DiedInfo(BaseModel):
    """
    优抚一件事-优抚政策-抚恤政策
    """

    IDENTITY_TYPE_CHOICES = (
        ("0", "民警"),
        ("1", "辅警"),
    )

    POLITICAL_CLASS = (
        ("0", "慰问金"),
        ("1", "保险金"),
        ("2", "五险一金"),
        ("3", "抚恤金"),
        ("4", "住院医疗"),
    )

    IS_ = (

    PENSION_TYPE_CHOICES = (
        ("0", "因公牺牲"),
        ("1", "病故"),
        ("2", "伤残"),
        ("3", "重病"),
        ("4", "困难"),
        ("5", "住院"),
    )


    policer_number = models.CharField(max_length=100, verbose_name="警号", null=True, blank=True, help_text="警号")
    name = models.CharField(max_length=100, verbose_name="姓名", null=True, blank=True, help_text="姓名")
    gender = models.CharField(max_length=1, default='0', verbose_name="性别", null=True, blank=True, choices=GENDER_CHOICES, help_text="性别")
    id_card = models.CharField(max_length=100, verbose_name="身份证号", db_index=True, null=True, blank=True, unique=True, help_text="身份证号")
    birth_date = models.DateField(verbose_name="出生日期", null=True, blank=True, help_text="出生日期")
    nation = models.CharField(max_length=100, verbose_name="民族", null=True, blank=True, help_text="民族")
    pension_type = models.CharField(max_length=5, default='0', verbose_name="抚恤类别", null=True, blank=True, choices=PENSION_TYPE_CHOICES, help_text="抚恤类别")
    identity_type = models.CharField(max_length=2, default='0', verbose_name="身份", null=True, blank=True, choices=IDENTITY_TYPE_CHOICES, help_text="身份")
    job_level = models.CharField(max_length=100, verbose_name="职务职级", null=True, blank=True, help_text="职务职级")
    dept_name = models.CharField(max_length=100, verbose_name="单位名称", null=True, blank=True, help_text="单位名称")
    work_date = models.DateField(verbose_name="参公时间", null=True, blank=True, help_text="参公时间")
    political_status = models.CharField(max_length=5, default='0', verbose_name="政治面貌", null=True, blank=True, help_text="政治面貌", choices=POLITICAL_STATUS_CHOICES)
    brief_achievements = models.TextField(verbose_name="简要事迹", null=True, blank=True, help_text="简要事迹")
    policy_name = models.CharField(max_length=100, verbose_name="对应政策", null=True, blank=True, help_text="对应政策")
    remark = models.TextField(verbose_name="备注", null=True, blank=True, help_text="备注")


    class Meta:
        db_table = "pension_personal_info"
        verbose_name = "优抚一件事-人员管理-基本信息"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.name or ""
