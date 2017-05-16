#!/bin/bash
export http_proxy=http://10.8.0.1:8080
export https_proxy=https://10.8.0.1:8080
export ftp_proxy=http://10.8.0.1:8080
export socks_proxy=http://10.8.0.1:8080
export all_proxy=http://10.8.0.1:8080
sudo rm /etc/apt/apt.conf
sudo touch /etc/apt/apt.conf
sudo sh -c 'echo Acquire::http::proxy \"http://10.8.0.1:8080\"; >> /etc/apt/apt.conf'
sudo sh -c 'echo Acquire::https::proxy \"http://10.8.0.1:8080\"; >> /etc/apt/apt.conf'
sudo sh -c 'echo Acquire::ftp::proxy \"http://10.8.0.1:8080\"; >> /etc/apt/apt.conf'
sudo sh -c 'echo Acquire::socks::proxy \"http://10.8.0.1:8080\"; >> /etc/apt/apt.conf'
sudo apt-get install curl
sudo apt-get install python-pip
sudo -H pip install mechanize
sudo apt-get install python-tk


