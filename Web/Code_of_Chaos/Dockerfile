FROM ruby

RUN apt-get update 

WORKDIR /var/www/html
COPY . .
RUN bundle install

EXPOSE 4567
CMD ["bundle", "exec", "rackup", "--host", "0.0.0.0", "-p", "4567"]