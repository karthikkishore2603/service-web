FROM ubuntu

CMD [ "/bin/bash" ]

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install mysql-server -y
RUN apt-get install mysql-client -y
RUN service mysql start