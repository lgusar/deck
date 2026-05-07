from textual import work
from textual.app import ComposeResult
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from deck import server_service
from deck.server_service import Server, StatsResponse


class ServerStatsLabel(Widget):
    server: Server
    response: reactive[StatsResponse | None] = reactive(None)

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.server = server

    @work(exclusive=True)
    async def fetch_stats(self) -> None:
        self.response = await server_service.get_stats(self.server)

    def on_mount(self) -> None:
        self.fetch_stats()
        self.set_interval(1, self.fetch_stats)

    def _update_label(self, id: str, text: str) -> None:
        formatted_id = id.replace("-", " ").replace("#", "")
        label = self.query_one(id, Label)
        label.update(f"{formatted_id.capitalize():<15} {text}")
        label.remove_class("hidden")

    def watch_response(self, value) -> None:
        if self.response is not None:
            try:
                self.query_one("#placeholder-label", Label).remove()
            except NoMatches:
                pass

            self._update_label("#last-seen", f"{self.response.timestamp}")
            self._update_label(
                "#response-time",
                f"{self.response.response_time:0.2f}s",
            )
            self._update_label("#status", f"{self.response.status.value}")

            self._update_label("#cpu-usage", f"{self.response.cpu_usage * 100:.2f}%")
            self._update_label(
                "#memory-usage", f"{self.response.memory_usage * 100:.2f}%"
            )
            self._update_label("#disk-usage", f"{self.response.disk_usage * 100:.2f}%")

    def compose(self) -> ComposeResult:
        yield Label(f"{'IP:':<15} {self.server.ip}", id="ip")
        yield Label(f"{'Role:':<15} {self.server.role}", id="role")
        yield Label(f"{'Environment:':<15} {self.server.env}", id="env")

        yield Label("Fetching status", id="placeholder-label")

        yield Label(id="last-seen", classes="hidden")
        yield Label(id="response-time", classes="hidden")
        yield Label(id="status", classes="hidden")

        yield Label(id="cpu-usage", classes="hidden")
        yield Label(id="memory-usage", classes="hidden")
        yield Label(id="disk-usage", classes="hidden")
