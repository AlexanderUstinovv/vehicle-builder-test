import uuid

from aiohttp import web

from app.service.vehicle_service import get_vehicle_info

router = web.RouteTableDef()


@router.get("/api/{vehicle_id}")
async def fetch_get(request: web.Request) -> web.Response:
    try:
        vehicle_id = uuid.UUID(request.match_info.get("vehicle_id", None))
    except Exception:
        raise web.HTTPBadRequest()
    vehicle = await get_vehicle_info(vehicle_id)
    if vehicle:
        return web.json_response(vehicle)
    raise web.HTTPNotFound()
