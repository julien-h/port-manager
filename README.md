# port-manager

A server to manage ports available on localhost. The server binds to `127.0.0.1:5000` and distributes ports in the range `[5001:6000]`.

## Installation

Create a virtual environment in the project's directory as follows:

```
python -m venv venv
source venv/bin/activate
pip install -r python-requirements.txt
```

## Usage

To start the server, run the script `port_manager.sh`.

Open http://127.0.0.1:5000 in your browser to see the list of reserved ports.

To obtain a free port, run the script `client/port-get.sh $NAME` (replace `$NAME` with a custom name for the port):

```
export port=$(port-get.sh "jupyter")
```

To put the port back, use `client/port-putback.sh $PORT`:

```
port-putback.sh $PORT
```
