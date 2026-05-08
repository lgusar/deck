from textual.app import ComposeResult
from textual.widget import Widget

from deck.server_service import Server
from deck.ssh.ssh_connection import ServerConnection
from deck.tui.server_command_panel import ServerCommandPanel
from deck.tui.server_stats_label import ServerStatsLabel


class ServerWidget(Widget):
    connection: ServerConnection

    DEFAULT_CSS = """
    ServerWidget {
        layout: grid;
        grid-size: 4 1;
        grid-gutter: 1;
    }

    ServerCommandPanel {
        column-span: 3;
    }
    """

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.connection = ServerConnection(server)

    def compose(self) -> ComposeResult:
        yield ServerStatsLabel(self.connection)
        yield ServerCommandPanel()

    async def on_mount(self) -> None:
        await self.connection.connect()

    async def on_dismount(self) -> None:
        await self.connection.disconnect()

    def refresh_stats(self) -> None:
        self.query_one(ServerStatsLabel).fetch_stats()

    def execute_command(self, command: str) -> None:
        self.query_one(ServerCommandPanel).execute_command(self.connection, command)
