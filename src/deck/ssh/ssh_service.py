import logging
import re
import time
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing_extensions import Any

from deck.ssh.ssh_connection import ServerConnection


class ServerStatus(Enum):
    UP = "UP"
    DOWN = "DOWN"


@dataclass
class StatsResponse:
    timestamp: datetime
    status: ServerStatus
    response_time: float
    cpu_usage: float | None
    memory_usage: float | None
    disk_usage: float | None


class Status(Enum):
    SUCCESS = "Success"
    ERROR = "Error"


@dataclass
class CommandResponse:
    status: Status
    output: str


logger = logging.getLogger("deck.ssh_service")


async def execute_command(
    connection: ServerConnection, command: str
) -> AsyncGenerator[CommandResponse, Any]:

    proc = await connection.conn.create_process(command)

    async for line in proc.stdout:
        yield CommandResponse(Status.SUCCESS, line)

    async for line in proc.stderr:
        yield CommandResponse(Status.ERROR, line)


async def get_stats(connection: ServerConnection) -> StatsResponse | None:
    start_time = time.monotonic()

    cpu_usage: float | None = None
    memory_usage: float | None = None
    disk_usage: float | None = None
    try:
        cpu_usage = await _get_cpu_usage(connection)
        memory_usage = await _get_memory_usage(connection)
        disk_usage = await _get_disk_usage(connection)
        status = ServerStatus.UP
    except Exception as e:
        logger.error(e)
        status = ServerStatus.DOWN

    end_time = time.monotonic()

    response_time = end_time - start_time
    return StatsResponse(
        datetime.now(),
        status,
        response_time,
        cpu_usage,
        memory_usage,
        disk_usage,
    )


async def _get_cpu_usage(connection: ServerConnection) -> float:

    async def _read_cpu(connection: ServerConnection) -> str:
        output = ""
        async for result in execute_command(
            connection, "top -bn1 | grep '%Cpu' || top -bn1 | grep 'Cpu(s)'"
        ):
            output += result.output

        return output

    output = await _read_cpu(connection)

    match = re.search(r"(\d+(?:\.\d+)?)\s*id", output)

    if not match:
        raise ValueError(f"Could not parse CPU output: {output}")

    idle = float(match.group(1))

    return 100.0 - idle


async def _get_memory_usage(connection: ServerConnection) -> float:
    async def _read_memory_usage(connection: ServerConnection) -> str:
        output = ""
        async for result in execute_command(connection, "free -m"):
            output += result.output

        return output

    def _parse_memory_usage(input: str) -> float:
        lines = input.splitlines()
        memory_line = lines[1].split()

        total = float(memory_line[1])
        used = float(memory_line[2])

        return used / total

    output = await _read_memory_usage(connection)
    return _parse_memory_usage(output)


async def _get_disk_usage(connection: ServerConnection) -> float:

    async def _read_disk_usage(connection: ServerConnection) -> str:
        output = ""
        async for result in execute_command(connection, "df -B1 /"):
            output += result.output

        return output

    def _parse_disk_usage(input: str) -> float:
        lines = input.splitlines()
        disk_line = lines[1].split()

        total = float(disk_line[1])
        used = float(disk_line[2])

        return used / total

    output = await _read_disk_usage(connection)
    return _parse_disk_usage(output)
