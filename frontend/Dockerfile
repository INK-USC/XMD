FROM node:16-alpine as build

COPY . /frontend
WORKDIR /frontend

RUN npm install
RUN npm run-script build


FROM nginx
RUN mkdir /app
COPY --from=build /frontend/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
