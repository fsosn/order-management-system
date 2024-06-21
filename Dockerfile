FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["sh", "-c", "\
    if [ ! -d 'migrations' ]; then \
    flask db init; \
    fi && \
    flask db stamp head && \
    flask db migrate && \
    flask db upgrade && \
    flask run --host=0.0.0.0 --port=5000 \
    "]