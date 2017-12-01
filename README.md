# supsnap-server

## about
the api server for surprise-snap. match users in the same place, order to supsnap-camera-server to take a snapshot, receive snapshot from it, and broadcast snapshot to users.

## install
* setup docker and docker-compose environment
  * [Install Docker](https://docs.docker.com/engine/installation/)
  * [Install Docker Compose](https://docs.docker.com/compose/install/)
  * [Dockerコマンドをsudoなしで実行する方法](https://qiita.com/DQNEO/items/da5df074c48b012152ee)
* make linux user and ssh key for portforwarding
* edit sshd_config (allow remote port forwarding on other than local loopback)
  * vi /etc/ssh/sshd_config
  * add `GatewayPorts yes`
  * sudo /etc/init.d/sshd restart

## usage

### initial build
    ./build.sh

at docker-compose version 1.14.0, docker-compose run `docker-compose build` automatically if container have not built yet. so you can skip this step by your docker-compose environment.

### run
    ./run.sh

### reset db
    ./kill_db.sh

## apis
all http request method is POST

### get place
    POST /get_place

get place by beacon data

### get visiter
    POST /visiter

get visiter by beacon and user data

### delete visiter
    POST /delete_visiter

delete visiter by visiter data

### get image
    POST /get_image

get full size image by visiter data

### get thum
    POST /get_thum

get thumbnail by visiter data

### get snap state
    POST /get_snap_state

get latest supsnap informations by visiter data

## support debugging
below functions available when **only debug mode**.

    app.run(debug=True)

### api tester(simple http client)
access document-root of supsnap-server

### debugging api
you can get each models informations

    GET /models/(Beacon|Place|Snap|Visiter)

get all data in each models

    GET /models/(Beacon|Place|Snap|Visiter)/(id)

get one data
