FROM python:3.10
LABEL authors="novikor"

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry install --no-root


EXPOSE 3000

ENTRYPOINT ["poetry", "run", "python", "main.py"]
