FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1
COPY requirements.txt entry_point_fastapi.sh .env ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app
EXPOSE 8200
ENTRYPOINT ["/bin/sh", "entry_point_fastapi.sh"]