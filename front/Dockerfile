# build stage
FROM node:lts-alpine as build-stage

WORKDIR /app
COPY ./src/package*.json ./
RUN npm install
COPY ./src .

ARG API_URL
ENV API_URL=${API_URL}

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# Served by node version

#FROM node:10-alpine
#
## create destination directory
#RUN mkdir -p /usr/src/nuxt-app
#WORKDIR /usr/src/nuxt-app
#
## copy package.json and install dependencies
#COPY src/package*.json /usr/src/nuxt-app/
#RUN npm install
#
## copy the app, note .dockerignore
#COPY src /usr/src/nuxt-app/
#
#ARG AUTH_ENDPOINT
#ENV AUTH_ENDPOINT=${AUTH_ENDPOINT}
#
#ARG API_URL
#ENV API_URL=${API_URL}
#
## create production-ready build
#RUN npm run build
#
## expose 3000 on container
#EXPOSE 3000
#
## set app serving to permissive / assigned
#ENV NUXT_HOST=0.0.0.0
## set app port
#ENV NUXT_PORT=3000
#
## start the app
#CMD [ "npm", "start" ]
