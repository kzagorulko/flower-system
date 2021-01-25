FROM nikolaik/python-nodejs

RUN apt-get update

# install nginx
RUN apt-get -y install nginx
RUN apt-get install gettext-base

# deploy preparing
COPY ./deployment/ /deployment/

# frontend dependencies
ARG FRONT_API_URL
ENV REACT_APP_API_URL=$FRONT_API_URL

COPY ./frontend/package.json ./frontend/package-lock.json /frontend/

RUN cd /frontend/ && npm install

COPY ./frontend/ /frontend

RUN cd /frontend/ && npm run build

# backend dependencies
COPY ./backend/requirements.txt /backend/

RUN cd /backend/ && python3 -m venv .venv
RUN /bin/bash -c "source /backend/.venv/bin/activate"
RUN cd /backend/ && python3 -m pip install -r requirements.txt

COPY ./backend/ /backend

# nginx
ADD ./deployment/nginx/nginx.conf /etc/nginx/

# applying migrations, nginx and python running
CMD /bin/bash -c "envsubst '\$PORT' < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp" \
 && mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf && nginx \
 && chmod +x ./deployment/scripts/deploy_backend.sh && ./deployment/scripts/deploy_backend.sh

