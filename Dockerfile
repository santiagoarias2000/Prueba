FROM python:3.8-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
# Ejecutar la inicialización de la base de datos
RUN python db_init.py

CMD ["python", "product_service.py"]