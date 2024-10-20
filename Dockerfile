FROM python:3.10-alpine
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "appserver:gunicorn_app"]