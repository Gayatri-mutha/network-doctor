import socket
import time


def check_internet():
    """Check internet connectivity using a TCP connection."""

    try:
        start = time.perf_counter()

        connection = socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )

        connection.close()

        elapsed = (time.perf_counter() - start) * 1000

        return {
            "status": True,
            "message": "Internet connection detected",
            "time": round(elapsed, 2)
        }

    except OSError:
        return {
            "status": False,
            "message": "No internet connection detected",
            "time": None
        }