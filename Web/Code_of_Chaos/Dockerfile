FROM ruby

WORKDIR /var/www/html

COPY Gemfile* ./

RUN bundle install

COPY . .

EXPOSE 4567

CMD ["bundle", "exec", "rackup", "--host", "0.0.0.0", "-p", "4567"]