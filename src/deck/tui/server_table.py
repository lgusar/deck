import logging

from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Collapsible, Input

from deck.server_service import Server
from deck.tui.server_widget import ServerWidget

logger = logging.getLogger("deck.server_table")


class ServerTable(ScrollableContainer):
    BINDINGS = [
        ("j", "move_down", "Next server"),
        ("k", "move_up", "Previous server"),
        ("space", "toggle_select", "Select server"),
        ("r", "refresh_stats", "Refresh"),
        ("x", "open_command_input", "Execute command"),
        ("/", "show_filter", "Filter"),
        ("escape", "hide_filter", "Clear filter"),
    ]

    servers: list[Server]
    selected: set[Collapsible] = set()

    def __init__(self, servers: list[Server]) -> None:
        super().__init__()
        self.servers = servers

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Filter by hostname", classes="hidden", id="filter")
        yield Input(placeholder="Execute command", classes="hidden", id="command")
        for server in self.servers:
            # TODO: ignore duplicate servers
            with Collapsible(collapsed=True, title=server.hostname, classes="box"):
                yield ServerWidget(server)

    def action_refresh_stats(self) -> None:
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

    def _apply_filter(self, query: str) -> None:
        for collapsible in self.query(Collapsible):
            if query.lower() in collapsible.title:
                collapsible.remove_class("hidden")
            else:
                collapsible.add_class("hidden")

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

    def action_show_filter(self) -> None:
        input = self.query_one("#filter", Input)
        input.remove_class("hidden")
        input.focus()

    def action_hide_filter(self) -> None:
        input = self.query_one("#filter", Input)
        input.clear()
        input.add_class("hidden")

        collapsibles = list(self.query(Collapsible))
        if collapsibles is None:
            return

        collapsibles[0].query_one("CollapsibleTitle").focus()

    def action_open_command_input(self) -> None:
        # TODO: add validators
        input = self.query_one("#command", Input)
        input.remove_class("hidden")
        input.focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "filter":
            self._apply_filter(event.value)

    def on_input_submitted(self, event: Input.Changed) -> None:
        if event.input.id == "command":
            input = self.query_one("#command", Input)

            for widget in self.selected:
                if isinstance(widget, Collapsible):
                    server_widget = widget.query_one(ServerWidget)
                    server_widget.execute_command(input.value)
                    widget.collapsed = False

            input.clear()
            input.add_class("hidden")

            collapsibles = list(self.query(Collapsible))
            if collapsibles is None:
                return

            collapsibles[0].query_one("CollapsibleTitle").focus()
