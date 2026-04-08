#!/usr/bin/env python3
"""
Ghost Agency API entry point.
"""

import uvicorn
import asyncio
import signal
import sys
from ghostagency.api.main import app


async def run_server():
    """Run the uvicorn server indefinitely."""
    config = uvicorn.Config(
        "ghostagency.api.main:app", host="0.0.0.0", port=8000, log_level="info"
    )
    server = uvicorn.Server(config)

    # Setup signal handlers
    loop = asyncio.get_event_loop()

    def signal_handler():
        print("\nReceived shutdown signal, stopping server...")
        server.should_exit = True

    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, signal_handler)

    await server.serve()


if __name__ == "__main__":
    print("Starting Ghost Agency API server...")
    print("Server will run on http://0.0.0.0:8000")
    print("Press Ctrl+C to stop the server")

    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer shutdown complete.")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)
