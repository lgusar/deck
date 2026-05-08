from __future__ import annotations

import logging

from textual import work
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import RichLog

from deck.ssh.ssh_connection import ServerConnection
from deck.ssh.ssh_service import execute_command

logger = logging.getLogger("deck.server_command_panel")


class ServerCommandPanel(Widget, can_focus=True):
    def compose(self) -> ComposeResult:
        yield RichLog(auto_scroll=True, id="output")

    @work(exclusive=True)
    async def execute_command(self, connection: ServerConnection, command: str) -> None:
        log = self.query_one(RichLog)
        log.clear()
        async for result in execute_command(connection, command):
            log.write(result.output.strip(), scroll_end=True)
