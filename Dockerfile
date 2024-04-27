FROM python:3.11.5

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "ToDOlistApp.main:app", "--host", "0.0.0.0", "--port", "10000", "--reload"]
