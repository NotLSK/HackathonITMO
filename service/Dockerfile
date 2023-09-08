FROM tiangolo/uvicorn-gunicorn-fastapi

COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --default-timeout=99999
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install libzbar0 -y && pip install pyzbar
RUN pip install sentence-transformers --default-timeout=99999
RUN pip install pandas
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]