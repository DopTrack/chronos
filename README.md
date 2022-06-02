# Chronos

## Developer instructions

First, install the dependencies with conda:

```bash
git clone git@github.com:DopTrack/chronos.git
cd chronos
conda env create -f env.yml
conda activate chronos_env
```

Then, to build and test the django app, run

```bash
python chronos/manage.py runserver
```

The app can then be accessed locally at `127.0.0.1:8000`.

### Docker development environment
Install [Docker](https://docs.docker.com/get-docker/) and additionally for Linux, install [docker-compose](https://docs.docker.com/compose/install/).

To test the app in a docker environment, in the root of the repository, run

```bash
docker-compose up -d --build
```

The app can then be accessed at `127.0.0.1:8000`. 
>Check for erros in the logs if this doesn't work via `docker-compose logs -f`.

To close the service and remove any attached volumes, run

```bash
docker-compose down -v
```