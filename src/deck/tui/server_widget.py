from textual.app import ComposeResult
from textual.widget import Widget

from deck.server_service import Server
from deck.tui.server_info_label import ServerInfoLabel
from deck.tui.server_stats_label import ServerStatsLabel


class ServerWidget(Widget):
    server: Server

    DEFAULT_CSS = """
    ServerWidget {
        layout: grid;
        grid-size: 4 1;
        grid-gutter: 1;
    }
    """

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.server = server

    def compose(self) -> ComposeResult:
        yield ServerInfoLabel(self.server)
        yield ServerStatsLabel(self.server)

    def refresh_stats(self) -> None:
        self.query_one(ServerInfoLabel).fetch_status()
        self.query_one(ServerStatsLabel).fetch_stats()
