FROM node:lts-alpine AS base
RUN mkdir front
WORKDIR /front
COPY . ./
RUN npm install --no-package-lock
RUN npm run build
FROM nginx
RUN mkdir /html
COPY --from=base /front/build /html
COPY nginx_config.conf /etc/nginx/conf.d/default.conf
ENV REACT_APP_DATA_PANEL_API_URL="http://api.data-panel.lafabrica"