#!/usr/bin/env python3
"""
Ghost Agency API server - proper implementation that stays running.
"""

import uvicorn
import signal
import sys
from ghostagency.api.main import app


class Server:
    def __init__(self):
        self.should_exit = False
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def handle_signal(self, sig, frame):
        self.should_exit = True
        print(f"\nReceived signal {sig}, shutting down gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    server = Server()

    print("Starting Ghost Agency API server...")
    print("Dashboard available at: http://localhost:8000/")
    print("API documentation at: http://localhost:8000/api/docs")
    print("Press Ctrl+C to stop the server")

    config = uvicorn.Config(
        app, host="0.0.0.0", port=8000, log_level="info", reload=True
    )

    try:
        server_instance = uvicorn.Server(config)
        server_instance.run()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)
