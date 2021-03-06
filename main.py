from fastapi import FastAPI

from endpoints.v1.users.endpoints import user_routers
from endpoints.v1.product_categories.endpoints import product_categories_router
from endpoints.v1.products.endpoints import products_router
from endpoints.v1.machines.endpoints import machines_router

app = FastAPI(
    title="Vend API",
    description="Izrada REST API-a sa FastAPI & Pydantic",
    version="0.0.1",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

api_v1_prefix = "/api/v1"

app.include_router(user_routers, prefix=api_v1_prefix)
app.include_router(product_categories_router, prefix=api_v1_prefix)
app.include_router(products_router, prefix=api_v1_prefix)
app.include_router(machines_router, prefix=api_v1_prefix)
