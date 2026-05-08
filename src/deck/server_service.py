from pydantic import BaseModel


class Server(BaseModel):
    hostname: str
    ip: str
    role: str
    env: str
    ssh_user: str
    ssh_port: int


class Inventory(BaseModel):
    servers: list[Server]
