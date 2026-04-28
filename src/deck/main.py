import tomllib
from pathlib import Path

import typer
from pydantic import BaseModel
from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget
from textual.widgets import Collapsible, Footer, Header, Label

DEFAULT_PATH = "~/.config/deck/inventory.toml"


class Server(BaseModel):
    hostname: str
    ip: str
    role: str
    env: str
    ssh_user: str
    ssh_port: int


class Inventory(BaseModel):
    servers: list[Server]


typer_app = typer.Typer()


def main():
    typer_app()


@typer_app.command()
def run(inventory_path: str = DEFAULT_PATH):
    path = Path(inventory_path).expanduser()
    # TODO: decide what to do when inventory file doesn't exist
    if not path.exists():
        raise FileNotFoundError(f"Could not find inventory file in {path}")

    with open(path, "rb") as f:
        data = tomllib.load(f)

    inventory = Inventory.model_validate(data)

    app = DeckApp(inventory)
    app.run()


class ServerWidget(Widget):
    server: Server

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.server = server

    def render(self) -> RenderResult:
        self.border_title = self.server.hostname
        return str(self.server)


class DeckApp(App):
    CSS_PATH = "../../resources/deck.tcss"
    inventory: Inventory

    def __init__(self, inventory: Inventory) -> None:
        super().__init__()
        self.inventory = inventory

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        for server in self.inventory.servers:
            with Collapsible(collapsed=True, title=server.hostname, classes="box"):
                yield Label(str(server))

    def on_mount(self) -> None:
        self.title = "deck"
        self.theme = "tokyo-night"
