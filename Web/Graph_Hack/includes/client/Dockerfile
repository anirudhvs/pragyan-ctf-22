FROM node:slim

WORKDIR /usr/client

COPY package.json .
RUN npm install --force
COPY . .

EXPOSE 3000

CMD ["npm", "start"]