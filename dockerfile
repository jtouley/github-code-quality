FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r config/requirements.txt
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]