import asyncssh

from deck.server_service import Server


# TODO: add error handling
class ServerConnection:
    server: Server
    conn: asyncssh.SSHClientConnection

    def __init__(self, server) -> None:
        self.server = server

    async def connect(self) -> None:
        self.conn = await asyncssh.connect(
            self.server.ip, username=self.server.ssh_user, port=self.server.ssh_port
        )

    async def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            await self.conn.wait_closed()
