FROM python:3.11

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy
RUN pipenv install python-docx

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "prod"]
