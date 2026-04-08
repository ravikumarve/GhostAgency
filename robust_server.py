#!/usr/bin/env python3
"""
Robust Ghost Agency API server that stays running.
"""

import uvicorn
import signal
import sys
import time
from ghostagency.api.main import app


class RobustServer:
    def __init__(self):
        self.should_exit = False
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, sig, frame):
        print(f"\nReceived signal {sig}, shutting down gracefully...")
        self.should_exit = True
        sys.exit(0)

    def run(self):
        print("Starting Robust Ghost Agency API server...")
        print("Dashboard available at: http://localhost:8000/")
        print("API documentation at: http://localhost:8000/api/docs")
        print("Press Ctrl+C to stop the server")

        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            lifespan="off",  # Disable lifespan to prevent issues
        )

        server = uvicorn.Server(config)

        # Run server in a way that should keep it running
        import threading

        def server_thread():
            try:
                server.run()
            except Exception as e:
                print(f"Server error: {e}")

        thread = threading.Thread(target=server_thread, daemon=True)
        thread.start()

        # Keep main thread alive
        try:
            while not self.should_exit:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    server = RobustServer()
    server.run()
