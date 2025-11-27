from datetime import datetime
from typing import Annotated

from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class Operator(Base):

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    load_limit: Mapped[int] = mapped_column(default=10)  # максимальное количество активных обращений

    source_weights: Mapped[list["OperatorSourceWeight"]] = relationship("OperatorSourceWeight", back_populates="operator")
    contacts: Mapped[list["Contact"]] = relationship("Contact", back_populates="operator")


class Lead(Base):

    id: Mapped[intpk]
    external_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)  # уникальный идентификатор лида
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(11), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    contacts: Mapped[list["Contact"]] = relationship("Contact", back_populates="lead")


class Source(Base):

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    source_weights: Mapped[list["OperatorSourceWeight"]] = relationship("OperatorSourceWeight", back_populates="source")
    contacts: Mapped[list["Contact"]] = relationship("Contact", back_populates="source")


class OperatorSourceWeight(Base):

    id: Mapped[intpk]
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    weight: Mapped[int] = mapped_column(default=1)  # вес оператоора для этого источника

    operator: Mapped["Operator"] = relationship("Operator", back_populates="source_weights")
    source: Mapped["Source"] = relationship("Source", back_populates="source_weights")


class Contact(Base):

    id: Mapped[intpk]
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=True)
    message: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)  # активно ли обращение
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    lead: Mapped["Lead"] = relationship("Lead", back_populates="contacts")
    source: Mapped["Source"] = relationship("Source", back_populates="contacts")
    operator: Mapped["Operator"] = relationship("Operator", back_populates="contacts")
