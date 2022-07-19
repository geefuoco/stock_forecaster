FROM python:3.10
WORKDIR /app
RUN pip install --upgrade pip
RUN mkdir ./api
RUN mkdir ./dist

ADD api ./api
ADD dist ./dist
WORKDIR /app/api
RUN pip install -r ./requirements.txt
ENV FLASK_ENV production

EXPOSE 3000
CMD ["gunicorn", "-b", ":3000", "server:app"]
