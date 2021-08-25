from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Column,
    Integer, String, Unicode, Date,
    DateTime,
    Table,
)
from sqlalchemy.orm import relationship

from db import Base, metadata

company_user_table = Table(
    'user_company',
    metadata,
    Column('user_id', ForeignKey('user_contact.user_id'), primary_key=True),
    Column('company_id', ForeignKey('company.company_id'), primary_key=True),
    Column('job_title', Unicode(100)),
)


class User(Base):
    __tablename__ = 'user_contact'

    user_id = Column('user_id', Integer, primary_key=True)
    first_name = Column('first_name', Unicode(50), nullable=False)
    last_name = Column('last_name', Unicode(50), nullable=False)
    birth_day = Column('birth_day', Date, nullable=True)
    # one to many
    contacts = relationship("Contact", back_populates="user")

    # many to many
    companies = relationship(
        "Company",
        secondary=company_user_table,
        back_populates="workers"
    )


class Contact(Base):
    __tablename__ = 'contact'
    contact_id = Column('contact_id', Integer, primary_key=True)
    email = Column('email', String(50), nullable=False)
    cell_phone = Column('cell_phone', String(50), nullable=False)
    address = Column('address', Unicode(200), nullable=True)

    # relationship
    user_id = Column(Integer, ForeignKey('user_contact.user_id'), nullable=True)
    user = relationship("User", back_populates="contacts")


class Company(Base):
    __tablename__ = 'company'
    company_id = Column('company_id', Integer, primary_key=True)
    name = Column('name', Unicode(100), nullable=True)
    domain_name = Column('domain_name', String(100), nullable=True)
    description = Column('description', Unicode(200), nullable=True)
    founded = Column(
        'founded',
        DateTime,
        nullable=True,
        default=datetime.utcnow,
    )

    # relationship
    workers = relationship(
        "User",
        secondary=company_user_table,
        back_populates="companies"
    )
