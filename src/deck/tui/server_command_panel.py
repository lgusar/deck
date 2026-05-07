from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Placeholder

from deck.server_service import Server


class ServerCommandPanel(Widget):
    server: Server

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.server = server

    def compose(self) -> ComposeResult:
        yield Placeholder()
        yield Placeholder()
