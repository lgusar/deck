from textual import work
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder, RichLog

from deck.ssh.ssh_connection import ServerConnection
from deck.ssh.ssh_service import execute_command


class ServerCommandPanel(Widget):
    DEFAULT_CSS = """
        ServerCommandPanel {
            layout: grid;
            grid-size: 8 1;
        }

        #output {
            column-span: 7;
        }
    """

    def compose(self) -> ComposeResult:
        yield Placeholder(id="result")
        yield RichLog(auto_scroll=True, id="output")

    @work(exclusive=True)
    async def execute_command(self, connection: ServerConnection, command: str) -> None:
        log = self.query_one(RichLog)
        log.clear()
        async for result in execute_command(connection, command):
            log.write(result.output.strip(), scroll_end=True)
