"""
server.py

Handles websocket server connection and high-level functions.

Author: Nathan SV
Created: 05-05-2025
Last Updated: 05-05-2025
"""

import asyncio
import signal
import websockets
from loguru import logger
from colorama import Fore, Style
from client import Client


class Server:
    """Manage server start / stop and handle clients"""

    # Main function
    def __init__(self, host, port):
        """Initialize server parameters"""
        self.host = host
        self.port = port
        self.list_client = []
        self.queue = asyncio.Queue()
        self.shutdown_event = asyncio.Event()
        self.server = None

    def start(self):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self.handler_shutdown)
        loop.run_until_complete(self.run())

    # Subfunction
    def handler_shutdown(self):
        """Manage Ctrl+C input to gracefully stop the server."""
        asyncio.create_task(self.shutdown())

    async def run(self):
        """Run the WebSocket server."""
        self.server = await websockets.serve(self.handler_client, self.host, self.port)
        logger.success(
            f"Server running on {Fore.GREEN}ws://{self.host}:{self.port}{Fore.GREEN}"
        )
        print("---------------------------------------------")
        await self.server.wait_closed()

    async def handler_client(self, websocket, path=None):
        """Handle an incoming WebSocket client connection."""
        # Add client
        client = Client(websocket)
        client.start()
        self.list_client.append(client)
        logger.connection(websocket.remote_address)

        # Wait for the client to disconnect by awaiting the event
        await client.disconnection.wait()

        # Perform necessary cleanup after client is disconnected
        logger.disconnection(websocket.remote_address)
        self.list_client.remove(client)

    async def shutdown(self):
        """Gracefully shut down the server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("---------------------------------------------")
            logger.success(f"Server shutdown")

        # Filter out inactive clients and then close them
        for client in list(self.list_client):
            if client.is_active:
                await client.close()

        self.list_client.clear()
