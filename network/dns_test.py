import socket
import time


def dns_test(domain="example.com"):
    """Measure DNS resolution time."""

    try:
        start = time.perf_counter()

        socket.getaddrinfo(
            domain,
            80,
            type=socket.SOCK_STREAM
        )

        elapsed = (time.perf_counter() - start) * 1000

        return {
            "success": True,
            "time": round(elapsed, 2),
            "domain": domain
        }

    except socket.gaierror:
        return {
            "success": False,
            "time": None,
            "domain": domain
        }