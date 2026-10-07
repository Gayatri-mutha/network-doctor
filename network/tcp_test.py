import socket
import time


def tcp_test(host, port):
    """Test TCP connectivity to a specific service."""

    try:

        start = time.perf_counter()

        connection = socket.create_connection(
            (host, port),
            timeout=3
        )

        connection.close()

        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": True,
            "time": round(elapsed, 2)
        }

    except OSError:

        return {
            "success": False,
            "time": None
        }