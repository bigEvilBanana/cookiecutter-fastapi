{%- if cookiecutter.use_sentry == 'y' %}
import sentry_sdk{% endif %}
from fastapi import FastAPI
{%- if cookiecutter.use_sentry == 'y' %}
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware{% endif %}
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router as api_router_v1
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

{%- if cookiecutter.use_sentry == 'y' %}
if not settings.SENTRY_DSN:
    raise EnvironmentError('Please put SENTRY_DSN to your environment')

sentry_sdk.init(dsn=settings.SENTRY_DSN)
app.add_middleware(SentryAsgiMiddleware)
{% endif %}

app.include_router(api_router_v1, prefix=settings.API_V1_STR)
