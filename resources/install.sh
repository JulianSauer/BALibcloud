#!/bin/bash
mkdir /home/logs
apt-get update
apt-get install maven git openjdk-7-jdk -y > /home/logs/install.txt
git clone https://github.com/ewolff/user-registration.git /home/app/ > /home/logs/git.txt
mvn -f /home/app/user-registration-application/pom.xml spring-boot:run > /home/logs/mvn.txt