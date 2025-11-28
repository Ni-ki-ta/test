from typing import List
from fastapi import APIRouter

from services import ContactService
from schemas.contact import ContactSchema, ContactResponseSchema, ContactCreateSchema
from src.database import DBSession

contact_router = APIRouter(prefix="/contact", tags=["contact"])


@contact_router.post("/", response_model=ContactResponseSchema)
async def create_contact(
        contact: ContactCreateSchema,
        db: DBSession
):
    return await ContactService.create_contact(db, contact)


@contact_router.get("/", response_model=List[ContactSchema])
async def list_contacts(db: DBSession):
    return await ContactService.get_all_contacts(db)
