from fastapi import APIRouter

from routers.contact import contact_router
from routers.lead import lead_router
from routers.operator import operator_router
from routers.operator_source_weight import operator_source_weight_router
from routers.source import source_router

api_router = APIRouter()

api_router.include_router(contact_router)
api_router.include_router(lead_router)
api_router.include_router(operator_router)
api_router.include_router(operator_source_weight_router)
api_router.include_router(source_router)
