import random
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shemas.contact import ContactSchema, ContactResponseSchema, ContactCreateSchema
from shemas.operator import OperatorSchema
from src.models import Lead, Contact, Operator, OperatorSourceWeight


class LeadService:
    @staticmethod
    async def find_or_create_lead(
            db: AsyncSession, external_id: str, email: str = None, phone: str = None
    ) -> Lead:
        """ Поиск или создание Lead по external_id """
        result = await db.execute(select(Lead).filter(Lead.external_id == external_id))

        lead = result.scalar_one_or_none()
        if not lead:
            lead = Lead(external_id=external_id, email=email, phone=phone)
            db.add(lead)
            await db.commit()
            await db.refresh(lead)
        return lead


class DistributionService:
    @staticmethod
    async def get_operator_load(
            db: AsyncSession, operator_id: int
    ) -> int:
        """ Получение текущей нагрузки оператора """
        result = await db.execute(
            select(Contact).filter(
                Contact.operator_id == operator_id,
                Contact.is_active == True
            ))
        return len(result.scalars().all())

    @staticmethod
    async def select_operator(
            db: AsyncSession, source_id: int
    ) -> Optional[Operator]:
        """ Выбор оператора для источника с учётом весов и лимитов"""
        result = await db.execute(
            select(OperatorSourceWeight)
            .filter(OperatorSourceWeight.source_id == source_id)
            .join(Operator)
            .filter(Operator.is_active == True)
        )
        weights_query = result.scalars().all()

        if not weights_query:
            return None

        avalaible_operators = []
        avalaible_weights = []

        for weights_record in weights_query:
            current_load = await DistributionService.get_operator_load(db, weights_record.operator_id)
            if current_load < weights_record.operator.load_limit:
                avalaible_operators.append(weights_record.operator)
                avalaible_weights.append(weights_record.weight)

        if not avalaible_operators:
            return None

        total_weight = sum(avalaible_weights)
        rand_val = random.uniform(0, total_weight)
        cumulative = 0

        for i, weight in enumerate(avalaible_weights):
            cumulative += weight
            if rand_val <= cumulative:
                return avalaible_operators[i]

        return avalaible_operators[0]


class ContactService:
    @staticmethod
    async def create_contact(
            db: AsyncSession, contact_data: ContactCreateSchema
    ) -> ContactResponseSchema:
        """ Создание обращения и распределение оператора """
        lead = await LeadService.find_or_create_lead(
            db,
            contact_data.lead_external_id
        )

        operator = await DistributionService.select_operator(db, contact_data.source_id)

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

        contact_schema = ContactSchema.from_orm(contact)
        operator_schema = OperatorSchema.from_orm(operator) if operator else None

        return ContactResponseSchema(
            contact=contact_schema,
            operator=operator_schema
        )
