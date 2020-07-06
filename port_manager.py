import socket, errno
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Template
import logging

app = FastAPI()

ports = list(range(5001, 6000, 1))
sockets = {}
reserved_ports = {}

def bind_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("0.0.0.0", port))
        s.listen(1)
        return s
    except:
        s.close()
        raise


@app.on_event("startup")
async def startup_event():
    for port in ports:
        try:
            sockets[port] = bind_port(port)
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print(f"Port {port} is already in use")
            else:
                raise


@app.on_event("shutdown")
async def shutdown_event():
    for port in sockets:
        try:
            sockets[port].close()
        except:
            logging.exception(f'When closing port {port}')
            

@app.get("/", response_class=HTMLResponse)
async def index():
    template = Template("""
    <html><body><h1>List of reserved ports:</h1><table>
    {% for (port, str) in reserved_ports.items() %}
    <ul>
        <li><a href="http://127.0.0.1:{{port}}/"> {{ port }}:{{ str }} </a> [[ <a href="putback/{{port}}"> cancel </a> ]] </li>
    </ul>
    {% else %}
    <p> No reserved ports </p>
    {% endfor %}
    </table></body></html>
    """)
    return template.render(reserved_ports=reserved_ports)

@app.get("/get/{name}")
async def get_any_port(name: str):
    for port in sorted(sockets.keys()):
        if await get_port(name, port):
            return port
    return -1


@app.get("/get/{name}/{port_id}")
async def get_port(name: str, port_id: int):
    s = sockets.pop(port_id, None)
    if s:
        s.close()
        reserved_ports[port_id] = name
        return True
    else:
        return False


@app.get("/putback/{port_id}")
async def putback_port(port_id: int):
    try:
        if port_id not in reserved_ports:
            return (False, "Port was not reserved through the manager.")  
        elif port_id in sockets:
            return (False, "Port already acquired by the manager, this shouldn't have happened.")
        else:
            sockets[port_id] = bind_port(port_id)
            reserved_ports.pop(port_id, None)
            return (True, "ok")
    except Exception as e:
        logging.exception('When attempting to bind port')
        return (False, f'{e!r}')


@app.get("/list")
async def list_reserved_ports():
    return reserved_ports


if __name__=='__main__':
    import uvicorn
    uvicorn.run(app, port=5000)