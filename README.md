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

The app can then be accessed locally at 127.0.0.1:8000