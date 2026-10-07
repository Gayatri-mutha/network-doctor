def diagnose_network(results):
    """
    Analyze network test results and return problems,
    possible causes, and recommendations.
    """

    problems = []
    recommendations = []

    # Internet connectivity
    if not results.get("internet", False):
        problems.append("Internet connection is unavailable.")
        recommendations.append(
            "Check your Wi-Fi/mobile connection and restart the router if needed."
        )

    # Latency
    latency = results.get("latency")

    if latency is not None:
        if latency > 200:
            problems.append(
                f"High network latency detected ({latency} ms)."
            )
            recommendations.append(
                "Move closer to the router, reduce network traffic, "
                "or check with your Internet Service Provider."
            )
        elif latency > 100:
            problems.append(
                f"Moderate network latency detected ({latency} ms)."
            )
            recommendations.append(
                "Check other devices using the network and consider "
                "reducing background downloads."
            )

    # Packet loss
    packet_loss = results.get("packet_loss")

    if packet_loss is not None:
        if packet_loss >= 10:
            problems.append(
                f"High packet loss detected ({packet_loss}%)."
            )
            recommendations.append(
                "Check Wi-Fi signal strength, router stability, "
                "and possible network congestion."
            )
        elif packet_loss > 0:
            problems.append(
                f"Some packet loss detected ({packet_loss}%)."
            )
            recommendations.append(
                "Check your wireless connection and network stability."
            )

    # DNS
    if not results.get("dns", False):
        problems.append("DNS resolution is not working correctly.")
        recommendations.append(
            "Try changing the DNS server to a reliable server such as "
            "Google DNS (8.8.8.8) or Cloudflare DNS (1.1.1.1)."
        )

    # Gateway
    if not results.get("gateway", False):
        problems.append("Default gateway is unreachable.")
        recommendations.append(
            "Check your connection to the router and restart the router."
        )

    # TCP services
    if not results.get("tcp", False):
        problems.append("TCP connectivity test failed.")
        recommendations.append(
            "Check firewall settings and verify that the network "
            "allows outbound TCP connections."
        )

    # No problems
    if not problems:
        problems.append("No major network problems detected.")
        recommendations.append(
            "Your network appears healthy. No immediate action is required."
        )

    return {
        "problems": problems,
        "recommendations": recommendations
    }