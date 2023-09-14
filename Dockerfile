FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY server/ .
COPY processing/ .
COPY entrypoint.sh .

CMD ["./entrypoint.sh"]

