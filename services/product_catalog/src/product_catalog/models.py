from datetime import datetime
from decimal import Decimal

from sqlalchemy import JSON, Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from bss_shared.db import DecimalText, UtcDateTime


class Base(DeclarativeBase):
    pass


offering_category = Table(
    "offering_category",
    Base.metadata,
    Column("offering_id", ForeignKey("product_offering.id"), primary_key=True),
    Column("category_id", ForeignKey("category.id"), primary_key=True),
)

offering_price = Table(
    "offering_price",
    Base.metadata,
    Column("offering_id", ForeignKey("product_offering.id"), primary_key=True),
    Column("price_id", ForeignKey("product_offering_price.id"), primary_key=True),
)


class Lifecycle:
    """Columns every TMF620 resource shares."""

    version: Mapped[str] = mapped_column(default="1.0")
    lifecycle_status: Mapped[str]
    valid_from: Mapped[datetime | None] = mapped_column(UtcDateTime)
    valid_to: Mapped[datetime | None] = mapped_column(UtcDateTime)
    last_update: Mapped[datetime] = mapped_column(UtcDateTime)


class Catalog(Lifecycle, Base):
    __tablename__ = "catalog"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    catalog_type: Mapped[str | None]

    categories: Mapped[list["Category"]] = relationship(back_populates="catalog")


class Category(Lifecycle, Base):
    __tablename__ = "category"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    is_root: Mapped[bool] = mapped_column(default=False)
    catalog_id: Mapped[str | None] = mapped_column(ForeignKey("catalog.id"))
    parent_id: Mapped[str | None] = mapped_column(ForeignKey("category.id"))

    catalog: Mapped[Catalog | None] = relationship(back_populates="categories")
    parent: Mapped["Category | None"] = relationship(
        back_populates="children", remote_side=[id]
    )
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
    offerings: Mapped[list["ProductOffering"]] = relationship(
        secondary=offering_category, back_populates="categories"
    )


class ProductSpecification(Lifecycle, Base):
    __tablename__ = "product_specification"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    brand: Mapped[str | None]
    product_number: Mapped[str | None]
    is_bundle: Mapped[bool] = mapped_column(default=False)

    characteristics: Mapped[list["SpecCharacteristic"]] = relationship(
        back_populates="specification", order_by="SpecCharacteristic.id"
    )


class SpecCharacteristic(Base):
    __tablename__ = "spec_characteristic"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    specification_id: Mapped[str] = mapped_column(
        ForeignKey("product_specification.id")
    )
    name: Mapped[str]
    description: Mapped[str | None]
    value_type: Mapped[str]
    values: Mapped[list[str]] = mapped_column(JSON, default=list)

    specification: Mapped[ProductSpecification] = relationship(
        back_populates="characteristics"
    )


class ProductOfferingPrice(Lifecycle, Base):
    __tablename__ = "product_offering_price"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price_type: Mapped[str]
    price_value: Mapped[Decimal | None] = mapped_column(DecimalText)
    price_unit: Mapped[str | None]
    recurring_charge_period_type: Mapped[str | None]
    recurring_charge_period_length: Mapped[int | None]
    uom_amount: Mapped[Decimal | None] = mapped_column(DecimalText)
    uom_units: Mapped[str | None]


class ProductOffering(Lifecycle, Base):
    __tablename__ = "product_offering"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    is_bundle: Mapped[bool] = mapped_column(default=False)
    is_sellable: Mapped[bool] = mapped_column(default=True)
    specification_id: Mapped[str | None] = mapped_column(
        ForeignKey("product_specification.id")
    )

    specification: Mapped[ProductSpecification | None] = relationship()
    categories: Mapped[list[Category]] = relationship(
        secondary=offering_category, back_populates="offerings"
    )
    prices: Mapped[list[ProductOfferingPrice]] = relationship(
        secondary=offering_price, order_by="ProductOfferingPrice.id"
    )
