FROM python:3.11

ENV PHYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt ./

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "runserver"]