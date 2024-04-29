FROM node:20-slim

COPY . /app
WORKDIR /app


RUN npm install
RUN npm run build

EXPOSE 3000
CMD [ "npm", "run", "serve" ]