from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from deck.server_service import Inventory
from .server_table import ServerTable


class DeckApp(App):
    DEFAULT_CSS = """
        ServerTable {
            height: 100%;
            width: 100%;
        }

        ServerWidget {
            height: auto
        }

        Button {
            color: $primary;
        }

        .selected {
            background: $input-selection-background;
        }

        .hidden {
            display: none;
        }

        ServerCommandPanel {
            row-span: 3;
        }
        """
    inventory: Inventory

    def __init__(self, inventory: Inventory) -> None:
        super().__init__()
        self.inventory = inventory

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ServerTable(self.inventory.servers)

    def on_mount(self) -> None:
        self.title = "deck"
        self.theme = "tokyo-night"
