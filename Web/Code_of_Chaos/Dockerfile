FROM ruby:3.1.0-alpine

RUN apk update \
    && apk add --virtual build-dependencies build-base

WORKDIR /var/www/html

COPY Gemfile* ./

RUN gem install websocket-driver -v '0.7.5' --source 'https://rubygems.org/'

RUN bundle install

COPY . .

EXPOSE 4567

CMD ["bundle", "exec", "rackup", "--host", "0.0.0.0", "-p", "4567"]
