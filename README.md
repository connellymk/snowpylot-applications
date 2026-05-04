# snowpylot-applications
Using SnowPylot to investigate research questions

## Environment setup

Use Python 3.13 for this project. Avoid Python 3.14 for now, because it can
trigger a `matplotlib` recursion error in notebook plots.

Create and activate the virtual environment, then install the project requirements:

```bash
cd /Users/marykate/Desktop/Snow/snowpylot-applications
UV_CACHE_DIR=/tmp/uv-cache uv venv --python 3.13.11 --seed sp-app
source sp-app/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

If the virtual environment already exists, you can just activate it and install the requirements:

```bash
cd /Users/marykate/Desktop/Snow/snowpylot-applications
source sp-app/bin/activate
python3 -m pip install -r requirements.txt
```
