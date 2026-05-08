import logging
import tomllib
from pathlib import Path

import typer

from deck.server_service import Inventory
from deck.tui.deck_app import DeckApp

DEFAULT_PATH = "~/.config/deck/inventory.toml"


typer_app = typer.Typer()

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger("deck")
logging.getLogger("asyncssh").setLevel(logging.ERROR)


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
