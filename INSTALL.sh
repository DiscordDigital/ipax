#!/bin/bash

CentOs=yum
Ubuntu=apt-get


        # Installing Docker and Compile ipax on CentOS
        # Detect OS
        if [ -x /usr/bin/$CentOs ]; then
        echo "Installing Docker and Compiling ipax on CentOS"
sudo yum check-update;
curl -fsSL https://get.docker.com/ | sh &&
sudo systemctl start docker &&
docker build -t ipax:latest .

			# Installing Docker and compiling ipax Ubuntu
			# Detect OS
                elif [ -x /usr/bin/$Ubuntu ]; then
                echo "Installing Docker and Compiling ipax on Ubuntu"

# Command to install docker.
sudo apt-get update &&
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release &&
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg &&
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null &&
sudo apt-get update; sudo apt-get install -y docker-ce docker-ce-cli containerd.io &&
# compile ipax
docker build -t ipax:latest .
fi
