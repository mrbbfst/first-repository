from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String

from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from sqlalchemy import Table
from sqlalchemy.orm import Mapped, relationship

Base = declarative_base()
associate_table = Table(
    "check_products",
    Base.metadata,
    Column("check_id", ForeignKey("check.id")),
    Column("product_id", ForeignKey("product.id"))
)
class Check(Base):
    __tablename__ = 'check'
    id=Column(Integer, primary_key=True)
    time=Column(DateTime(), default=datetime.now)
    items = relationship('Product', secondary=associate_table)
    amount=Column(Integer, nullable=False)

class Product(Base):
    __tablename__ = 'product'
    id=Column(Integer, primary_key=True)
    title=Column(String(100), nullable=False)
    price=Column(Integer, nullable=False)
    barcode=Column(String(100), nullable=False)
    count=Column(Integer, nullable=False)
    guarantee=Column(Integer, nullable=False)

engine = create_engine("sqlite:///db.sqlite", echo=True)
Base.metadata.create_all(engine)