FROM php:7.4.5-apache

RUN apt-get update && apt-get upgrade -y && apt-get install sudo && \
    mkdir /var/www/html/response

COPY index.html /var/www/html

COPY ./response/index.html /var/www/html/response
