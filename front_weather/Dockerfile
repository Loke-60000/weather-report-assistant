FROM node:alpine

WORKDIR /app

COPY index.html style.css script.js /app/

EXPOSE 3000

RUN npm install -g http-server

CMD ["http-server", "-p", "3000"]