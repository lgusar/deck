import asyncio
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from enum import Enum
from typing_extensions import Any

from deck.server_service import Server


class Status(Enum):
    SUCCESS = "Success"
    ERROR = "Error"


@dataclass
class CommandResponse:
    status: Status
    output: str


async def execute_command(
    server: Server, command: str
) -> AsyncGenerator[CommandResponse, Any]:
    for c in command:
        yield CommandResponse(Status.SUCCESS, c)
        await asyncio.sleep(1)
