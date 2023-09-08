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
