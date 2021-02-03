# The Cat

Python API application

## Installation of dependencies

command to set up the stable repository
```bash
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io
```

## Usage

```bash
cd thecat/infra

#initialize docker swarm
sudo docker swarm init

#deploy stack
sudo docker stack deploy -c docker-compose.yml case

```

Running local, access the url 127.0.0.1:5000

If you are running in the cloud like EC2, you must update the postman collection host to the instance IP

Paths and token access are in the postman's collection

## License
[MIT](https://choosealicense.com/licenses/mit/)
