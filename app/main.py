from aiohttp import web
from api.routes import vehicle_router


async def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(vehicle_router)
    return app


web.run_app(init_app())
