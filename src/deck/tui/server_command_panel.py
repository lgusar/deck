from textual import work
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder, RichLog

from deck.server_service import Server
from deck.ssh.ssh import execute_command


class ServerCommandPanel(Widget):
    server: Server
    DEFAULT_CSS = """
        ServerCommandPanel {
            layout: grid;
            grid-size: 8 1;
        }

        #output {
            column-span: 7;
        }
    """

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.server = server

    def compose(self) -> ComposeResult:
        yield Placeholder(id="result")
        yield RichLog(auto_scroll=True, id="output")

    @work(exclusive=True)
    async def execute_command(self, command: str) -> None:
        log = self.query_one(RichLog)
        log.clear()
        async for result in execute_command(self.server, command):
            log.write(result.output)
