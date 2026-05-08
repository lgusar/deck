from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from deck.server_service import Server
from deck.ssh.ssh import CommandResponse
from deck.tui.server_command_panel import ServerCommandPanel
from deck.tui.server_stats_label import ServerStatsLabel


class ServerWidget(Widget):
    server: Server
    response: reactive[CommandResponse | None] = reactive(None)

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
        self.server = server

    def compose(self) -> ComposeResult:
        yield ServerStatsLabel(self.server)
        yield ServerCommandPanel(self.server)

    def refresh_stats(self) -> None:
        self.query_one(ServerStatsLabel).fetch_stats()

    def watch_response(self) -> None:
        if self.response is not None:
            label = self.query_one("#command", Label)
            text = f"Command status: {self.response.status.value}\n"
            text += f"Command output: {self.response.output}\n"
            label.update(text)
            label.remove_class("hidden")

    def execute_command(self, command: str) -> None:
        self.query_one(ServerCommandPanel).execute_command(command)
