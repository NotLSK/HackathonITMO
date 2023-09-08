from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from io import BytesIO
from PIL import Image

from src.database import get_async_session
from src.models import goods, shelves

app = FastAPI()


@app.post("/upload_shelf")
async def upload_shelf_image(file: UploadFile, db: AsyncSession = Depends(get_async_session)):
    try:
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))

        shelf_info = process_shelf_image(image)

        await save_shelf_info(db, shelf_info)

        return shelf_info
    except Exception as e:
        return {"error": str(e)}


@app.post("/upload_price_tag")
async def upload_price_tag_image(file: UploadFile, db: AsyncSession = Depends(get_async_session)):
    try:
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))

        price_tag_info = process_price_tag_image(image)

        existing_product = await get_product_by_barcode_or_name(db, price_tag_info["barcode"], price_tag_info["name"])

        if existing_product:
            return existing_product

        await save_price_tag_info(db, price_tag_info)
        return price_tag_info
    except Exception as e:
        return {"error": str(e)}


def process_shelf_image(image):
    goods = 4
    passes = 2
    size = 79.13

    return {"goods": goods, "passes": passes, "size": size}


def process_price_tag_image(image):
    barcode = "4650075427750"
    name = "Напиток безалкогольный ДОБРЫЙ Кола сгаз ПЭТ (Россия)"
    price = 150
    promo = True

    return {"barcode": barcode, "name": name, "price": price, "promo": promo}


async def save_shelf_info(db: AsyncSession, shelf_info: dict):
    async with db.begin() as transaction:
        query = shelves.insert().values(
            goods=shelf_info["goods"],
            passes=shelf_info["passes"],
            size=shelf_info["size"]
        )
        await db.execute(query)


async def get_product_by_barcode_or_name(db: AsyncSession, barcode: str, name: str):
    query = select(goods).where((goods.c.barcode == barcode) | (goods.c.name == name))
    result = await db.execute(query)
    product = result.fetchone()
    if product:
        return {
            "barcode": product.barcode,
            "name": product.name,
            "price": product.price,
            "promo": product.promo
        }
    else:
        return None


async def save_price_tag_info(db: AsyncSession, price_tag_info: dict):
    query = goods.insert().values(
        barcode=price_tag_info["barcode"],
        name=price_tag_info["name"],
        price=price_tag_info["price"],
        promo=price_tag_info["promo"]
    )
    await db.execute(query)
    await db.commit()

