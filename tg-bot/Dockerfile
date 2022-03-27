FROM python:3.9.12-bullseye
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./ /app
CMD ["sh", "-c",                                                                                                        \
     "sqlacodegen postgresql://south_coffee_user:pass@postgres:5432/south_coffee --schema southcoffee > models.py       \
      && python main.py"                                                                                                \
]
