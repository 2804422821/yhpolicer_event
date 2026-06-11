"""
优抚一件事-人员管理-基本信息视图集 - 增删改查、导入导出
"""
import tablib
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.decorators import action

from apps.business.personnel.app_personal_info.filters import PersonalInfoFilter
from apps.business.personnel.app_personal_info.models import PersonalInfo
from apps.business.personnel.app_personal_info.serializers import (
    PersonalInfoSerializer,
    PersonalInfoCreateSerializer,
    PersonalInfoUpdateSerializer,
    PersonalInfoResource,
)
from utils.json_response import DetailResponse, ErrorResponse
from utils.viewset import CustomModelViewSet


class PersonalInfoViewSet(CustomModelViewSet):
    """
    优抚一件事-人员管理-基本信息视图集
    """
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer
    create_serializer_class = PersonalInfoCreateSerializer
    update_serializer_class = PersonalInfoUpdateSerializer

    filterset_class = PersonalInfoFilter
    search_fields = ["policer_number", "name", "identity_type", "dept_name", "pension_type"]
    ordering = ["-create_datetime"]

    @action(detail=False, methods=["get"])
    def export_to_excel(self, request):
        """优抚人员基本信息导出"""
        resource = PersonalInfoResource()
        dataset = resource.export()
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        filename = f"personal_info_{timestamp}.xls"
        export_data = dataset.export("xls")
        response = HttpResponse(export_data, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=["post"])
    def import_from_excel(self, request):
        """优抚人员基本信息导入"""
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

        resource = PersonalInfoResource()
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
