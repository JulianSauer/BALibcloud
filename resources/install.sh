#!/bin/bash
apt-get update
apt-get install maven git openjdk-7-jdk -y
git clone https://github.com/ewolff/user-registration.git /home/ubuntu/app/
mvn -f /home/ubuntu/app/user-registration-application/pom.xml spring-boot:run