import subprocess
import platform
import re


def get_gateway():
    """Detect the default network gateway."""

    system = platform.system().lower()

    try:

        if system == "windows":

            result = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
                timeout=5
            )

            for line in result.stdout.splitlines():

                if "Default Gateway" in line:

                    parts = line.split(":")

                    if len(parts) > 1:

                        gateway = parts[-1].strip()

                        if gateway:
                            return gateway

        else:

            result = subprocess.run(
                ["ip", "route"],
                capture_output=True,
                text=True,
                timeout=5
            )

            match = re.search(
                r"default via ([\d.]+)",
                result.stdout
            )

            if match:
                return match.group(1)

        return "Unavailable"

    except Exception:
        return "Unavailable"


def ping_gateway(gateway):
    """Ping the detected gateway."""

    if gateway == "Unavailable":
        return None

    from .ping_test import ping_host

    result = ping_host(
        gateway,
        count=3
    )

    if result.get("success"):
        return result.get("average")

    return None