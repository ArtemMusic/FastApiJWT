"""
ФИКС ОШИБКИ ЗАГРУЗКИ ЭКРАНА (БЕЛЫЙ ЭКРАН) В http://127.0.0.1:8000/docs
ЕСЛИ СТРАНИЦА ДОКУМЕНТАЦИИ НЕ БУДЕТ ГРУЗИТЬСЯ, ТО ПОДКЛЮЧИТЬ ЭТОТ ФАЙЛ В МЕЙН И ЗАПУСКАТЬ create_app
"""

from contextlib import asynccontextmanager
from api_v1.users.views import router as user_router
from auth.views import router as auth_router

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from db.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await database.dispose()


def register_static_docs_routes(app: FastAPI):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
        )


def create_app(
        create_custom_static_urls: bool = False,
) -> FastAPI:
    app = FastAPI(
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        docs_url=None if create_custom_static_urls else "/docs",
        redoc_url=None if create_custom_static_urls else "/redoc",
    )

    app.include_router(prefix='/api/v1', router=user_router)
    app.include_router(router=auth_router)

    if create_custom_static_urls:
        register_static_docs_routes(app)
    return app
