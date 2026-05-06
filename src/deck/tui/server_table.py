from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Collapsible

from deck.server_service import Server
from deck.tui.server_widget import ServerWidget


class ServerTable(ScrollableContainer):
    BINDINGS = [
        ("j", "move_down", "Next server"),
        ("k", "move_up", "Previous server"),
        ("space", "toggle_select", "Select server"),
        ("r", "refresh_stats", "Refresh"),
    ]

    servers: list[Server]
    selected: set[Collapsible] = set()

    def __init__(self, servers: list[Server]) -> None:
        super().__init__()
        self.servers = servers

    def compose(self) -> ComposeResult:
        for server in self.servers:
            with Collapsible(collapsed=True, title=server.hostname, classes="box"):
                yield ServerWidget(server)

    def key_r(self) -> None:
        for widget in self.selected:
            if isinstance(widget, Collapsible):
                server_widget = widget.query_one(ServerWidget)
                server_widget.refresh_stats()

    def _get_focused_collapsible(self) -> Collapsible | None:
        focused = self.app.focused
        if focused is None:
            return None
        for ancestor in focused.ancestors_with_self:
            if isinstance(ancestor, Collapsible):
                return ancestor
        return None

    def _move_focus(self, direction: int) -> None:
        collapsibles = list(self.query(Collapsible))
        if not collapsibles:
            return

        current = self._get_focused_collapsible()
        if current is None:
            collapsibles[0].query_one("CollapsibleTitle").focus()
            return

        index = collapsibles.index(current)
        next = index + direction
        next = max(0, min(index + direction, len(collapsibles) - 1))
        collapsibles[next].query_one("CollapsibleTitle").focus()

        self.app.set_focus(collapsibles[next])

    def action_move_up(self) -> None:
        self._move_focus(-1)

    def action_move_down(self) -> None:
        self._move_focus(1)

    def action_toggle_select(self) -> None:
        current = self._get_focused_collapsible()
        if current is None:
            return

        if current in self.selected:
            self.selected.remove(current)
            current.remove_class("selected")
        else:
            self.selected.add(current)
            current.add_class("selected")
