FROM nikolaik/python-nodejs


# install Python 3
# RUN apt-get update && apt-get install -y python3.9 python3-pip
RUN apt-get update
# RUN apt-get -y install python3.7-dev
# RUN apt-get install python-psycopg2
# RUN apt-get -y install postgresql-server-dev-10 gcc python3-dev musl-dev curl sudo

# RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
# RUN apt-get install -y nodejs

# run up database

# install nginx
RUN apt-get -y install nginx
# RUN apt-get -y install python3-venv

COPY ./frontend/package.json ./frontend/package-lock.json /frontend/

RUN cd /frontend/ && npm install

COPY ./frontend/ /frontend

RUN cd /frontend/ && npm run build

COPY . .

ADD ./deployment/nginx/nginx.conf /etc/nginx/

RUN apt-get install gettext-base

CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp" && mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf && nginx && chmod +x ./deployment/scripts/deploy_backend.sh && ./deployment/scripts/deploy_backend.sh
