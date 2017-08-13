# supsnap-server

## about
the flask test app

## requirement
docker and docker-compose environment

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

### get visiter
    POST /visiter

get visiter from beacon and user

### get image
    POST /get_image

get full size image from visiter

### get thum
    POST /get_thum

get thumbnail from visiter

### get snap state
    POST /get_snap_state

get latest supsnap informations from visiter

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
