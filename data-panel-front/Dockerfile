FROM node:lts-alpine AS base
RUN mkdir front
WORKDIR /front
COPY data-panel-front ./
RUN npm install --no-package-lock
RUN npm run build
FROM nginx
RUN mkdir /html
COPY --from=base /front/build /html
COPY nginx_config.conf /etc/nginx/conf.d/default.conf