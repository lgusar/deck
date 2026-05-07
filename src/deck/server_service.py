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
class StatsResponse:
    timestamp: datetime
    status: Status
    response_time: float
    cpu_usage: float
    memory_usage: float
    disk_usage: float


async def get_stats(server: Server) -> StatsResponse | None:
    response_time = random.uniform(0.0, 1.0)
    cpu_usage = random.random()
    memory_usage = random.random()
    disk_usage = random.random()
    return StatsResponse(
        datetime.now(), Status.UP, response_time, cpu_usage, memory_usage, disk_usage
    )
