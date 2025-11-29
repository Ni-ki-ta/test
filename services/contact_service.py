import random
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from .source import SourceService
from src.models import Lead, Contact, Operator, OperatorSourceWeight
from schemas.contact import ContactCreateSchema, ContactResponseSchema, ContactSchema


class LeadService:
    @staticmethod
    async def find_or_create_lead(
            db: AsyncSession, external_id: str, email: str = None, phone: str = None
    ) -> Lead:
        result = await db.execute(
            select(Lead).where(Lead.external_id == external_id)
        )
        lead = result.scalar_one_or_none()

        if not lead:
            lead = Lead(external_id=external_id, email=email, phone=phone)
            db.add(lead)
            await db.commit()
            await db.refresh(lead)
        return lead


class DistributionService:
    @staticmethod
    async def get_operator_load(db: AsyncSession, operator_id: int) -> int:
        result = await db.execute(
            select(Contact).where(
                Contact.operator_id == operator_id,
                Contact.is_active == True
            )
        )
        contacts = result.scalars().all()
        return len(contacts)

    @staticmethod
    async def select_operator(db: AsyncSession, source_id: int) -> Optional[Operator]:
        result = await db.execute(
            select(OperatorSourceWeight)
            .where(OperatorSourceWeight.source_id == source_id)
            .join(Operator)
            .where(Operator.is_active == True)
            .options(selectinload(OperatorSourceWeight.operator))
        )
        weights_query = result.scalars().all()

        if not weights_query:
            return None

        available_operators = []
        available_weights = []

        for weight_record in weights_query:
            current_load = await DistributionService.get_operator_load(db, weight_record.operator_id)
            if current_load < weight_record.operator.load_limit:
                available_operators.append(weight_record.operator)
                available_weights.append(weight_record.weight)

        if not available_operators:
            return None

        total_weight = sum(available_weights)
        rand_val = random.uniform(0, total_weight)
        cumulative = 0

        for i, weight in enumerate(available_weights):
            cumulative += weight
            if rand_val <= cumulative:
                return available_operators[i]

        return available_operators[0]


class ContactService:
    @staticmethod
    async def create_contact(
            db: AsyncSession, contact_data: ContactCreateSchema
    ) -> ContactResponseSchema:
        source = await SourceService.get_source_by_id(db, contact_data.source_id)
        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source with id {contact_data.source_id} not found"
            )

        lead = await LeadService.find_or_create_lead(
            db,
            contact_data.lead_external_id
        )

        operator = await DistributionService.select_operator(db, contact_data.source_id)

        operator_data = None
        if operator:
            operator_data = {
                'id': operator.id,
                'name': operator.name,
                'is_active': operator.is_active,
                'load_limit': operator.load_limit,
                'current_load': await DistributionService.get_operator_load(db, operator.id)
            }

        contact = Contact(
            lead_id=lead.id,
            source_id=contact_data.source_id,
            operator_id=operator.id if operator else None,
            message=contact_data.message,
            is_active=True
        )

        db.add(contact)
        await db.commit()
        await db.refresh(contact)

        from schemas.contact import ContactSchema
        from schemas.operator import OperatorSchema

        contact_schema = ContactSchema(
            id=contact.id,
            lead_id=contact.lead_id,
            source_id=contact.source_id,
            operator_id=contact.operator_id,
            message=contact.message,
            is_active=contact.is_active,
            created_at=contact.created_at
        )

        operator_schema = None
        if operator_data:
            operator_schema = OperatorSchema(**operator_data)

        return ContactResponseSchema(
            contact=contact_schema,
            operator=operator_schema
        )

    @staticmethod
    async def get_all_contacts(db: AsyncSession) -> List[ContactSchema]:
        result = await db.execute(select(Contact))
        contacts = result.scalars().all()
        return [
            ContactSchema(
                id=contact.id,
                lead_id=contact.lead_id,
                source_id=contact.source_id,
                operator_id=contact.operator_id,
                message=contact.message,
                is_active=contact.is_active,
                created_at=contact.created_at
            )
            for contact in contacts
        ]
