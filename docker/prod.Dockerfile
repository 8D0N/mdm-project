FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app/src
# パスを通す
ENV PYTHONPATH=/app
USER 1000
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]