def calculate_score(results):
    """
    Calculate the Network Health score out of 100.
    """

    score = 0

    # Connectivity — 20 points
    if results.get("internet", False):
        score += 20

    # Latency — 20 points
    latency = results.get("latency")

    if latency is not None:
        if latency <= 50:
            score += 20
        elif latency <= 100:
            score += 15
        elif latency <= 200:
            score += 10
        elif latency <= 300:
            score += 5

    # Packet loss — 20 points
    packet_loss = results.get("packet_loss")

    if packet_loss is not None:
        if packet_loss == 0:
            score += 20
        elif packet_loss <= 2:
            score += 15
        elif packet_loss <= 5:
            score += 10
        elif packet_loss <= 10:
            score += 5

    # DNS — 15 points
    if results.get("dns", False):
        score += 15

    # Gateway — 10 points
    if results.get("gateway", False):
        score += 10

    # TCP — 10 points
    if results.get("tcp", False):
        score += 10

    # Network interface — 5 points
    if results.get("interface", True):
        score += 5

    return min(score, 100)


def generate_diagnosis(results):
    """
    Generate human-readable network diagnosis.
    """

    problems = []
    recommendations = []

    if not results.get("internet", False):
        problems.append("Internet connection is unavailable.")
        recommendations.append(
            "Check your Wi-Fi/mobile connection and restart the router."
        )

    latency = results.get("latency")

    if latency is not None:
        if latency > 200:
            problems.append(
                f"High latency detected ({latency} ms)."
            )
            recommendations.append(
                "Check network congestion, move closer to the router, "
                "or contact your Internet Service Provider."
            )
        elif latency > 100:
            problems.append(
                f"Moderate latency detected ({latency} ms)."
            )
            recommendations.append(
                "Reduce background network activity and check other "
                "devices using the connection."
            )

    packet_loss = results.get("packet_loss")

    if packet_loss is not None:
        if packet_loss >= 10:
            problems.append(
                f"High packet loss detected ({packet_loss}%)."
            )
            recommendations.append(
                "Check Wi-Fi signal strength, router stability, "
                "and network congestion."
            )
        elif packet_loss > 0:
            problems.append(
                f"Packet loss detected ({packet_loss}%)."
            )
            recommendations.append(
                "Check wireless signal quality and network stability."
            )

    if not results.get("dns", False):
        problems.append("DNS resolution is not working correctly.")
        recommendations.append(
            "Try using a reliable DNS server such as 8.8.8.8 "
            "or 1.1.1.1."
        )

    if not results.get("gateway", False):
        problems.append("Default gateway is unreachable.")
        recommendations.append(
            "Check the connection between your device and router."
        )

    if not results.get("tcp", False):
        problems.append("TCP connectivity test failed.")
        recommendations.append(
            "Check firewall settings and outbound TCP connectivity."
        )

    if not problems:
        problems.append("No major network problems detected.")
        recommendations.append(
            "Your network appears healthy. No immediate action is required."
        )

    return {
        "problems": problems,
        "recommendations": recommendations
    }


def diagnose_network(results):
    """
    Compatibility wrapper used by the automated tests.
    """

    return generate_diagnosis(results)