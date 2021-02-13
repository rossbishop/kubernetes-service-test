# Stage 0 - build React application
FROM tiangolo/node-frontend:10 as build-stage
WORKDIR /app
COPY package*.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build

# Stage 1 - Nginx server
FROM nginx:latest
COPY --from=build-stage /app/build/ /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf 
COPY ./secret/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY ./secret/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key
COPY ./secret/dhparam.pem /etc/ssl/certs/dhparam.pem
COPY ./self-signed.conf /etc/nginx/snippets/self-signed.conf
COPY ./ssl-params.conf /etc/nginx/snippets/ssl-params.conf
