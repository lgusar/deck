from textual import work
from textual.reactive import reactive
from textual.widgets import Static

from deck import server_service
from deck.server_service import Server, StatusResponse


class ServerInfoLabel(Static):
    server: Server
    status_response: reactive[StatusResponse | None] = reactive(None)

    def __init__(self, server: Server) -> None:
        super().__init__()
        self.server = server

    def on_mount(self) -> None:
        self.fetch_status()
        self.set_interval(10, self.fetch_status)

    @work(exclusive=True)
    async def fetch_status(self) -> None:
        response = await server_service.check_status(self.server)
        self.status_response = response

    def watch_status_response(self, value) -> None:
        self.update(self.render_text())

    def render_text(self) -> str:
        text = f"{'IP:':<15} {self.server.ip}\n"
        text += f"{'Role:':<15} {self.server.role}\n"
        text += f"{'Environment:':<15} {self.server.env}\n"
        if self.status_response:
            text += f"{'Last seen:':<15} {self.status_response.timestamp}\n"
            text += (
                f"{'Response time:':<15} {self.status_response.response_time:0.2f}s\n"
            )
            text += f"{'Status:':<15} {self.status_response.status.value}\n"
        else:
            text += "\n"
            text += "Fetching status...\n"

        return text
