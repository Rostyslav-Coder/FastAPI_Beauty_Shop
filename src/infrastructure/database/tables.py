"""src/infrastructure/database/tables.py"""

from typing import TypeVar

from sqlalchemy import (
    DATETIME,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

__all__ = ()

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class _Base:
    """Base class for all database models."""

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=_Base, metadata=meta)

ConcreteTable = TypeVar("ConcreteTable", bound=Base)  # type: ignore


class UsersTable(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False
    )
    phone_number: Mapped[str] = mapped_column(
        String(16), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    role: Mapped[Enum] = mapped_column(Enum("UserRole"), nullable=False)

    employee = relationship(
        "EmployeesTable", back_populates="user", uselist=False
    )


class EmployeesTable(Base):
    __tablename__ = "employees"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    profession: Mapped[Enum] = mapped_column(
        Enum("Profession"), nullable=False
    )
    working_days: Mapped[Enum] = mapped_column(
        Enum("WorkingDays"), nullable=False
    )
    working_shift: Mapped[Enum] = mapped_column(
        Enum("WorkingShift"), nullable=False
    )

    user = relationship("UsersTable", back_populates="employee")
    services = relationship("ServiceTable", back_populates="employee")
    bookings = relationship("BookingTable", back_populates="employee")


class ServiceTable(Base):
    __tablename__ = "services"

    name: Mapped[str] = mapped_column(String(length=32), nullable=False)
    title: Mapped[str] = mapped_column(String(length=500), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("employees.id"), nullable=False
    )

    employee = relationship("EmployeesTable", back_populates="services")
    bookings = relationship("BookingTable", back_populates="services")


class BookingTable(Base):
    __tablename__ = "bookings"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("employees.id"), nullable=False
    )
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services.id"), nullable=False
    )
    start_time: Mapped[DATETIME] = mapped_column(DATETIME, nullable=False)
    end_time: Mapped[DATETIME] = mapped_column(DATETIME, nullable=False)
    status: Mapped[Enum] = mapped_column(Enum("BookingStatus"), nullable=False)

    user = relationship("UsersTable")
    employee = relationship("EmployeesTable", back_populates="bookings")
    service = relationship("ServiceTable", back_populates="bookings")