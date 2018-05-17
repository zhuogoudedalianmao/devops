FROM httpd:2.4-alpine
ENV TZ=Asia/Shanghai

RUN echo $TZ > /etc/timezone
COPY ./Shanghai /etc/localtime
COPY ./Shanghai /usr/share/zoneinfo/Asia/Shanghai

COPY ./httpd.conf /usr/local/apache2/conf
COPY ./httpd-vhosts.conf /usr/local/apache2/conf/extra
COPY ./server.crt /usr/local/apache2/conf/server.crt
COPY ./server.key /usr/local/apache2/conf/server.key
#COPY ./index.html /usr/local/apache2/htdocs/index.html
#COPY ./index.html /var/www/html/index.html
