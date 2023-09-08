from fastapi import FastAPI, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from io import BytesIO
from PIL import Image

from src.database import get_async_session
from src.models import goods

from ml_models import CVPipeline, NLPPipeline

app = FastAPI()

cv_pipeline = CVPipeline()
nlp_pipeline = NLPPipeline()

@app.post("/upload_shelf")
async def upload_shelf_image(file: UploadFile, db: AsyncSession = Depends(get_async_session)):
    
    image_data = await file.read()
    image = Image.open(BytesIO(image_data))

    shelf_info = process_shelf_image(image)

    # await save_shelf_info(db, shelf_info)
    
    return shelf_info


@app.post("/upload_price_tag")
async def upload_price_tag_image(file: UploadFile, db: AsyncSession = Depends(get_async_session)):

    image_data = await file.read()
    image = Image.open(BytesIO(image_data))
    
    price_tag_info = process_price_tag_image(image)
    matching_result = match_product(price_tag_info['name'])
    price_tag_info['matched'] = False
    
    if matching_result:
        price_tag_info['name'] = matching_result
        price_tag_info['matched'] = True


    # await save_price_tag_info(db, price_tag_info)
    return price_tag_info



def process_shelf_image(image):
    
    shelf_objects = cv_pipeline.process_shelf(image)
    
    return shelf_objects


def process_price_tag_image(image):

    price_tag_info = cv_pipeline.process_price_tag(image)

    return price_tag_info


def match_product(name):
    in_base, _, base_name, _ = nlp_pipeline.match_name(name)

    if in_base:
        return base_name


async def save_price_tag_info(db: AsyncSession, price_tag_info: dict):
        query = goods.insert().values(
            barcode=price_tag_info["barcode"],
            name=price_tag_info["name"],
            price=price_tag_info["price"],
            promo=price_tag_info["promo"],
            matched=price_tag_info["matched"]
        )
        await db.execute(query)
        await db.commit()

async def save_shelf_info(db: AsyncSession, shelf_info: dict):
        query = goods.insert().values(
            total_items=shelf_info["total_items"],
            total_empty_space=shelf_info["total_empty_space"]
        )
        await db.execute(query)
        await db.commit()

