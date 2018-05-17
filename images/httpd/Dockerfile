FROM httpd:2.4-alpine
ENV TZ=Asia/Shanghai
RUN echo $TZ > /etc/timezone
COPY ./Shanghai /etc/localtime
COPY ./Shanghai /usr/share/zoneinfo/Asia/Shanghai

COPY ./httpd.conf /usr/local/apache2/conf
COPY ./httpd-vhosts.conf /usr/local/apache2/conf/extra
