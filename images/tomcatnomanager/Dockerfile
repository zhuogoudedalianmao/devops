FROM tomcat:7-jre8
ENV TZ=Asia/Shanghai
RUN echo $TZ > /etc/timezone
COPY ./Shanghai /etc/localtime
COPY ./Shanghai /usr/share/zoneinfo/Asia/Shanghai
COPY ./catalina.sh /usr/local/tomcat/bin
COPY ./context.xml /usr/local/tomcat/conf
COPY ./server.xml /usr/local/tomcat/conf
#COPY ./*.jar /usr/local/tomcat/lib/
COPY ./fonts /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/fonts
RUN chmod +x /usr/local/tomcat/bin/catalina.sh

