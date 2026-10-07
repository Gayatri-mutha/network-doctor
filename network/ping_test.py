import subprocess
import platform
import re
import time


def ping_host(host="8.8.8.8", count=5):
    """Measure latency and packet loss."""

    system = platform.system().lower()

    if system == "windows":
        command = [
            "ping",
            "-n",
            str(count),
            "-w",
            "1000",
            host
        ]
    else:
        command = [
            "ping",
            "-c",
            str(count),
            "-W",
            "1",
            host
        ]

    try:
        start = time.perf_counter()

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout

        times = []

        if system == "windows":
            matches = re.findall(
                r"time[=<]\s*(\d+)\s*ms",
                output,
                re.IGNORECASE
            )
        else:
            matches = re.findall(
                r"time[=<]\s*([\d.]+)\s*ms",
                output,
                re.IGNORECASE
            )

        for value in matches:
            try:
                times.append(float(value))
            except ValueError:
                pass

        if system == "windows":
            loss_match = re.search(
                r"(\d+)%\s*loss",
                output,
                re.IGNORECASE
            )
        else:
            loss_match = re.search(
                r"(\d+(?:\.\d+)?)%\s*packet loss",
                output,
                re.IGNORECASE
            )

        if loss_match:
            loss = float(loss_match.group(1))
        elif times:
            loss = ((count - len(times)) / count) * 100
        else:
            loss = 100

        elapsed = (time.perf_counter() - start) * 1000

        if times:
            return {
                "success": True,
                "min": round(min(times), 2),
                "max": round(max(times), 2),
                "average": round(sum(times) / len(times), 2),
                "packet_loss": round(loss, 2),
                "packets": len(times),
                "total": count,
                "elapsed": round(elapsed, 2)
            }

        return {
            "success": False,
            "min": None,
            "max": None,
            "average": None,
            "packet_loss": 100,
            "packets": 0,
            "total": count
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
            "min": None,
            "max": None,
            "average": None,
            "packet_loss": 100
        }