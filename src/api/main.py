import os
import django
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from api.routes import routers  # noqa

app = FastAPI(title="Crypto Blocks API", openapi_url="/api/v1/openapi.json", docs_url="/api/v1/docs")

for router in routers:
    app.include_router(router)
