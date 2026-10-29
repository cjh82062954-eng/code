FROM nginx:alpine
LABEL org.opencontainers.image.title="my-custom-nginx"
COPY app/ /usr/share/nginx/html/
EXPOSE 80
