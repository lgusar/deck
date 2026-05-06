import asyncio
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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


class Status(Enum):
    UP = "UP"
    DOWN = "DOWN"


@dataclass
class StatusResponse:
    timestamp: datetime
    status: Status


@dataclass
class StatsResponse:
    cpu_usage: float
    memory_usage: float
    disk_usage: float


async def check_status(server: Server) -> StatusResponse:
    return StatusResponse(timestamp=datetime.now(), status=Status.DOWN)


async def get_stats(server: Server) -> StatsResponse | None:
    return StatsResponse(0.15, 0.15, 0.15)
