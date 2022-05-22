from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db_mixins import IdTitleMixin, UserCreatedUpdatedMixin

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = (UniqueConstraint('email',  name='uc_user_email'),)

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)


class ProductCategory(IdTitleMixin, UserCreatedUpdatedMixin, Base):
    __tablename__ = "product_category"
    __table_args__ = (
        UniqueConstraint('title',  name='uc_product_category_title'),
    )

    products = relationship("Product", back_populates="product_category")


class Product(IdTitleMixin, UserCreatedUpdatedMixin, Base):
    __tablename__ = "product"
    __table_args__ = (UniqueConstraint('title',  name='uc_product_title'),)

    product_category_id = Column(Integer, ForeignKey("product_category.id"))

    product_category = relationship(
        "ProductCategory", back_populates="products")


class Machine(Base):
    __tablename__ = "machine"

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    model = Column(String(50), nullable=True)
    owner_id = Column(
        Integer, ForeignKey("user.id"), nullable=False)

    columns = relationship("MachineColumn", back_populates="machine")


class MachineColumn(Base):
    __tablename__ = "machine_column"
    __table_args__ = (
        UniqueConstraint(
            "machine_id", "index", name="uc_machine_column_machine_id_index"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    index = Column(Integer, index=True, nullable=False)
    current_quantity = Column(Integer, nullable=False)
    spiral_quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    machine_id = Column(Integer, ForeignKey("machine.id"), nullable=False)

    machine = relationship("Machine", back_populates="columns")
