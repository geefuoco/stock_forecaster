FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package*.json tsconfig.json tsconfig.node.json index.html vite.config.ts ./
COPY ./src ./src
COPY ./public ./public
RUN npm install
RUN npm run build


FROM python:3.10
WORKDIR /app
COPY --from=build-step /app/dist ./dist
RUN pip install --upgrade pip
RUN mkdir ./api

ADD api ./api
WORKDIR /app/api
RUN pip install -r ./requirements.txt
ENV FLASK_ENV production

EXPOSE 3000
CMD ["gunicorn", "-b", ":3000", "server:app"]
