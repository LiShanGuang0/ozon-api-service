from fastapi import APIRouter, Depends

from app.api.deps import OzonCredentials, get_ozon_credentials
from app.schemas.tasks import ImportTaskStatusResponse
from app.services.product_import import ProductImportService

router = APIRouter(prefix="/ozon/products", tags=["ozon-tasks"])


@router.get(
    "/import-tasks/{task_id}",
    response_model=ImportTaskStatusResponse,
    summary="查询商品创建/更新任务状态",
    description="转发 Ozon /v1/product/import/info，并将任务状态、product_id、错误信息回写到本地数据库。",
)
async def get_product_import_task(
    task_id: int,
    credentials: OzonCredentials = Depends(get_ozon_credentials),
) -> ImportTaskStatusResponse:
    return await ProductImportService().poll_import_task(task_id=task_id, credentials=credentials)
