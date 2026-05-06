import asyncio
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import random

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
    response_time: float


@dataclass
class StatsResponse:
    cpu_usage: float
    memory_usage: float
    disk_usage: float


async def check_status(server: Server) -> StatusResponse:
    response_time = random.uniform(0.0, 5.0)
    return StatusResponse(datetime.now(), Status.DOWN, response_time)


async def get_stats(server: Server) -> StatsResponse | None:
    return StatsResponse(0.15, 0.15, 0.15)
