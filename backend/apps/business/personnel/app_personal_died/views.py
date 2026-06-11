"""
优抚一件事-人员管理-病故人员视图集 - 增删改查、导入导出
"""
import tablib
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.decorators import action

from app_personal_info.models import PersonalInfo
from app_personal_info.serializers import PersonalInfoSerializer
from app_personal_died.filters import PersonalDiedFilter
from app_personal_died.models import PersonalDied
from app_personal_died.serializers import (
    PersonalDiedSerializer,
    PersonalDiedCreateSerializer,
    PersonalDiedUpdateSerializer,
    PersonalDiedResource,
)
from utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from utils.viewset import CustomModelViewSet


class PersonalDiedViewSet(CustomModelViewSet):
    """
    优抚一件事-人员管理-病故人员视图集
    """
    queryset = PersonalDied.objects.select_related("info").all()
    serializer_class = PersonalDiedSerializer
    create_serializer_class = PersonalDiedCreateSerializer
    update_serializer_class = PersonalDiedUpdateSerializer

    filterset_class = PersonalDiedFilter
    search_fields = [
        "info__policer_number", "info__name", "info__identity_type",
        "info__dept_name", "info__pension_type",
    ]
    ordering = ["-create_datetime"]

    @action(detail=False, methods=["get"])
    def available(self, request):
        """获取可选为病故人员的基本信息列表（抚恤类别为病故且未关联病故记录）"""
        died_info_ids = PersonalDied.objects.values_list("info_id", flat=True)
        queryset = PersonalInfo.objects.filter(
            pension_type="1"
        ).exclude(
            id__in=died_info_ids
        ).order_by("-create_datetime")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PersonalInfoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PersonalInfoSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def perform_destroy(self, instance):
        """删除病故人员时同时删除关联的基本信息（CASCADE 自动删除 PersonalDied）"""
        info_ids = [obj.info_id for obj in instance if obj.info_id]
        PersonalInfo.objects.filter(id__in=info_ids).delete()

    @action(detail=False, methods=["get"])
    def export_to_excel(self, request):
        """病故人员导出"""
        resource = PersonalDiedResource()
        dataset = resource.export(self.get_queryset())
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        filename = f"personal_died_{timestamp}.xls"
        export_data = dataset.export("xls")
        response = HttpResponse(export_data, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=["post"])
    def import_from_excel(self, request):
        """病故人员导入"""
        file = request.FILES.get("file")
        if not file:
            return ErrorResponse(msg="请上传文件")

        ext = file.name.rsplit(".", 1)[-1].lower()
        if ext not in ("xls", "xlsx"):
            return ErrorResponse(msg="仅支持 xls/xlsx 格式文件")

        try:
            if ext == "xlsx":
                dataset = tablib.Dataset().load(file.read(), format="xlsx")
            else:
                dataset = tablib.Dataset().load(file.read(), format="xls")
        except Exception:
            return ErrorResponse(msg="文件解析失败，请检查文件格式")

        resource = PersonalDiedResource()
        result = resource.import_data(dataset, dry_run=False, raise_errors=False)

        if result.has_errors():
            errors = []
            for row_errors in result.row_errors():
                line_num, errs = row_errors
                for err in errs:
                    errors.append(f"第{line_num}行: {str(err.error)}")
            return ErrorResponse(
                msg=f"导入完成但有 {len(errors)} 条错误",
                data={"errors": errors[:20]}
            )

        return DetailResponse(
            msg=f"导入成功，共导入 {result.total_rows} 条数据",
            data={"total": result.total_rows}
        )
