import tablib
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.decorators import action

from apps.business.app_reference.models import ReviewBasis
from apps.business.app_reference.serializers import (
    ReviewBasisSerializer,
    ReviewBasisCreateUpdateSerializer,
    ReviewBasisResource,
)
from utils.json_response import DetailResponse, ErrorResponse
from utils.viewset import CustomModelViewSet


class ReviewBasisViewSet(CustomModelViewSet):
    """
    执法案件质量-评查依据 视图集
    """

    queryset = ReviewBasis.objects.all()
    serializer_class = ReviewBasisSerializer
    create_serializer_class = ReviewBasisCreateUpdateSerializer
    update_serializer_class = ReviewBasisCreateUpdateSerializer

    filterset_fields = ["quality_type", "score_type"]
    search_fields = ["score_content"]
    ordering = ["-create_datetime"]

    @action(detail=False, methods=['get'])
    def export_to_excel(self, request):
        """
        评查依据导出
        """
        resource = ReviewBasisResource()
        dataset = resource.export()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        filename = f"review_basis_{timestamp}.xls"
        export_data = dataset.export('xls')
        response = HttpResponse(export_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=['post'])
    def import_from_excel(self, request):
        """
        评查依据导入
        """
        file = request.FILES.get('file')
        if not file:
            return ErrorResponse(msg="请上传文件")

        ext = file.name.rsplit('.', 1)[-1].lower()
        if ext not in ('xls', 'xlsx'):
            return ErrorResponse(msg="仅支持 xls/xlsx 格式文件")

        try:
            if ext == 'xlsx':
                dataset = tablib.Dataset().load(file.read(), format='xlsx')
            else:
                dataset = tablib.Dataset().load(file.read(), format='xls')
        except Exception:
            return ErrorResponse(msg="文件解析失败，请检查文件格式")

        resource = ReviewBasisResource()
        result = resource.import_data(dataset, dry_run=False, raise_errors=False)

        if result.has_errors():
            errors = []
            for row_idx, row_errors in enumerate(result.row_errors(), start=1):
                line_num, errs = row_errors
                for err in errs:
                    errors.append(f"第{line_num}行: {str(err.error)}")
            return ErrorResponse(msg=f"导入完成但有 {len(errors)} 条错误", data={"errors": errors[:20]})

        return DetailResponse(
            msg=f"导入成功，共导入 {result.total_rows} 条数据",
            data={"total": result.total_rows}
        )
