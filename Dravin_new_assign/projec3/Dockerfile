FROM python:3.11.2

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 4000

CMD [ "uvicorn","run:app","--reload" ]
