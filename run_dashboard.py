#!/usr/bin/env python3
"""
Ghost Agency Dashboard Runner
This script keeps the server running persistently.
"""

import uvicorn
import signal
import sys
import time
from ghostagency.api.main import app


class DashboardServer:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def handle_signal(self, sig, frame):
        print(f"\nReceived signal {sig}, shutting down...")
        self.running = False
        sys.exit(0)

    def run(self):
        print("=" * 60)
        print("GHOST AGENCY DASHBOARD SERVER")
        print("=" * 60)
        print("Dashboard: http://localhost:8000/")
        print("Agents:    http://localhost:8000/agents")
        print("Clients:   http://localhost:8000/clients")
        print("Stats:     http://localhost:8000/stats")
        print("API Docs:  http://localhost:8000/api/docs")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        print("=" * 60)

        # Configure and run uvicorn
        config = uvicorn.Config(
            app, host="0.0.0.0", port=8000, log_level="info", lifespan="off"
        )

        server = uvicorn.Server(config)

        # Run server in a separate process to keep it alive
        import multiprocessing

        def run_server():
            server.run()

        # Start server process
        server_process = multiprocessing.Process(target=run_server)
        server_process.daemon = True
        server_process.start()

        # Keep main process alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        finally:
            if server_process.is_alive():
                server_process.terminate()
                server_process.join()


if __name__ == "__main__":
    server = DashboardServer()
    server.run()
