FROM python:3.12-alpine
RUN #apk add --no-cache dcron
ENV PYTHONUNBUFFERED=1
COPY requirements.txt entry_point_fastapi.sh .env ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app
#RUN echo "*/30 * * * * cd / && /usr/local/bin/python -m app.db_sync.worker >> /var/log/cron.log 2>&1" > /tmp/crontab
#RUN crontab /tmp/crontab
#RUN touch /var/log/cron.log
EXPOSE 8200
ENTRYPOINT ["/bin/sh", "entry_point_fastapi.sh"]