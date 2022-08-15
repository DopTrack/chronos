# Chronos

Chronos is a Django web app for scheduling measurements on the TU Delft DopTrack lab. The app makes use of [Django cms](https://www.django-cms.org/en/) for content creation.


## Developer instructions

### Webappserver
Install [Docker](https://docs.docker.com/get-docker/) and additionally for Linux, install [docker-compose](https://docs.docker.com/compose/install/).

To test the app in a docker environment, in the root of the repository, run

```bash
docker-compose up -d --build
```

The app can then be accessed at `127.0.0.1:8000`. 

>Check for erros in the logs if this doesn't work via `docker-compose logs -f`.

To close the service, run

```bash
docker-compose down
```

### Remote server
For development and testing, build and run the Docker image in the folder `/server`. To build the Docker image, in the root of the respository execute

```bash
docker build ./server/ -t doptrack_server
```

To run the image and open the bash terminal:
```bash
docker run --rm -it doptrack_server bash
```

To test the remote services in the `doptrack_server` container, run

```bash
bash setup_services.sh
```

You can verify the services running with `ps -ef`
