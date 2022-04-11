# ewoksserver

Backend for [ewoksweb](https://gitlab.esrf.fr/workflow/ewoks/ewoksweb)

## Development

Install from source

```bash
python -m pip install -e .[dev]
```

Run tests

```bash
pytest
```

Launch the backend

```bash
ewoks-server
```

## Configuration

The configuration keys are uppercase variables in a python script:

```python
# /tmp/config.py
RESOURCE_DIRECTORY = "/path/to/resource/directory/"
```

Specify the configuration file through the CLI

```bash
ewoks-server --configuration /tmp/config.py
```

or using the environment variable EWOKSSERVER_SETTINGS

```bash
export EWOKSSERVER_SETTINGS=/tmp/config.py
ewoks-server
```