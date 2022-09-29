FROM gitpod/workspace-mysql

RUN mysql -e "create user 'karthik'@'localhost' identified by 'password';"
RUN mysql -e "grant all priveleges on *.* to 'karthik'@'loaclhost';"
RUN mysql -e "create database service;"