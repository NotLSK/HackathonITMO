from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Boolean

metadata = MetaData()

goods = Table(
    "goods",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("barcode", String),
    Column("name", String),
    Column("price", Float),
    Column("promo", Boolean)
)

shelves = Table(
    "shelves",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("goods", Integer),
    Column("passes", Integer),
    Column("size", Float)
)
