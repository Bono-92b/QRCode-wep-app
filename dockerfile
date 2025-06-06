FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn qrcode pillow
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]