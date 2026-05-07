import asyncio
from dataclasses import dataclass
from enum import Enum

from deck.server_service import Server


class Status(Enum):
    SUCCESS = "Success"
    ERROR = "Error"


@dataclass
class CommandResponse:
    status: Status
    output: str


async def execute_command(server: Server, command: str) -> CommandResponse:
    return CommandResponse(Status.SUCCESS, command)
