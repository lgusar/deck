from textual import work
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from deck import server_service
from deck.server_service import Server, StatsResponse


class ServerStatsLabel(Widget):
    server: Server
    stats_response: reactive[StatsResponse | None] = reactive(None)

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.server = server

    @work(exclusive=True)
    async def fetch_stats(self) -> None:
        self.stats_response = await server_service.get_stats(self.server)

    def on_mount(self) -> None:
        self.fetch_stats()
        self.set_interval(10, self.fetch_stats)

    def watch_stats_response(self, value) -> None:
        if self.stats_response is not None:
            self.query_one("#cpu", expect_type=Label).update(
                f"CPU usage: {self.stats_response.cpu_usage}%"
            )
            self.query_one("#memory", expect_type=Label).update(
                f"Memory usage: {self.stats_response.memory_usage}%"
            )
            self.query_one("#disk", expect_type=Label).update(
                f"Disk usage: {self.stats_response.disk_usage}%"
            )
        else:
            self.query_one("#cpu", expect_type=Label).update("CPU usage: -")
            self.query_one("#memory", expect_type=Label).update("Memory usage: -")
            self.query_one("#disk", expect_type=Label).update("Disk usage: -")

    def compose(self) -> ComposeResult:
        yield Label("CPU usage: -", id="cpu")
        yield Label("Memory usage: -", id="memory")
        yield Label("Disk usage: -", id="disk")
