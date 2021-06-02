# How to configuration apps.

### Docker Image/Set up the repository:
```sh
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
$ echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Docker Image Install:
```sh
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Install Docker-Compose on Linux systems:
```sh
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

### Upgrade Docker-Compose on Linux systems:
```sh
$ docker-compose migrate-to-labels
```

### Docker-Compose Build:
```sh
$ cd /final_app #into location file
$ docker-compose build
```

### Start service:
```sh
$ docker-compose up
```

### After dock-compose up then need to config of mongodb replication:
```sh
1. Login to mongodb PRIMARY docker container
$ sudo docker exec -ti insert-mongodb /bin/bash

2. Activate mongo CLI
# mongo

3. (inside mongo cli) Set Variable config using replicaset Configuration above
> config = config={_id:"my-mongo-set",members:[{_id:0,host:"insert-mongodb:27017",priority:1},{_id:1,host:"query-mongodb:27017",priority:0}]};

4. (inside mongo cli) Initialize the config
> rs.initiate(config)

5. (inside mongo cli) Check if the config is successful
> rs.config()

Prevent Secondary from Becoming Primary
cfg = rs.conf()
cfg.members[1].priority = 0
rs.reconfig(cfg)

6. Quit from docker container
```

### Using apps:
```sh
1. Open browser and get url is 127.0.0.1 on web browser
2. Register
3. Login
4. Working
5. Logout
```
### Stop service:
```sh
$ docker-compose down
```
