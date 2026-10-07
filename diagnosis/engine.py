def latency_score(latency):

    if latency is None:
        return 0

    if latency < 30:
        return 20
    elif latency < 60:
        return 18
    elif latency < 100:
        return 15
    elif latency < 150:
        return 10
    elif latency < 200:
        return 5

    return 2


def packet_loss_score(loss):

    if loss is None:
        return 0

    if loss == 0:
        return 20
    elif loss <= 2:
        return 16
    elif loss <= 5:
        return 10

    return 3


def dns_score(dns_time):

    if dns_time is None:
        return 0

    if dns_time < 50:
        return 15
    elif dns_time < 100:
        return 12
    elif dns_time < 200:
        return 8

    return 4


def calculate_score(results):

    score = 0

    if results["internet"]["status"]:
        score += 20

    score += latency_score(
        results["ping"].get("average")
    )

    score += packet_loss_score(
        results["ping"].get("packet_loss")
    )

    score += dns_score(
        results["dns"].get("time")
    )

    gateway_latency = results.get(
        "gateway_latency"
    )

    if gateway_latency is not None:

        if gateway_latency < 20:
            score += 10
        elif gateway_latency < 50:
            score += 8
        elif gateway_latency < 100:
            score += 5
        else:
            score += 2

    tcp_success = sum(
        1
        for test in results["tcp"].values()
        if test["success"]
    )

    if tcp_success == 2:
        score += 10
    elif tcp_success == 1:
        score += 5

    if results["interface"]["local_ip"] != "Unavailable":
        score += 5

    return min(score, 100)


def generate_diagnosis(results):

    problems = []
    recommendations = []

    internet = results["internet"]
    ping = results["ping"]
    dns = results["dns"]

    if not internet["status"]:

        problems.append(
            "No internet connectivity detected."
        )

        recommendations.extend([
            "Check your Wi-Fi or Ethernet connection.",
            "Restart your router if necessary.",
            "Check whether other devices have internet access."
        ])

    else:

        if ping.get("average") is not None:

            if ping["average"] > 150:

                problems.append(
                    "High network latency detected."
                )

                recommendations.extend([
                    "Check whether other devices are using heavy bandwidth.",
                    "Move closer to the Wi-Fi router.",
                    "Try another network for comparison."
                ])

            elif ping["average"] > 100:

                problems.append(
                    "Moderately high network latency detected."
                )

        if ping.get("packet_loss", 0) > 5:

            problems.append(
                "Significant packet loss detected."
            )

            recommendations.extend([
                "Check Wi-Fi signal strength.",
                "Restart the router.",
                "Check for network congestion."
            ])

        elif ping.get("packet_loss", 0) > 2:

            problems.append(
                "Small amount of packet loss detected."
            )

        if dns.get("time") is not None:

            if dns["time"] > 200:

                problems.append(
                    "DNS resolution appears slow."
                )

                recommendations.append(
                    "Consider trying a different DNS server."
                )

    gateway_latency = results.get(
        "gateway_latency"
    )

    if gateway_latency is not None:

        if gateway_latency > 100:

            problems.append(
                "High latency to the local gateway detected."
            )

            recommendations.extend([
                "Check your Wi-Fi signal.",
                "Move closer to the router.",
                "Restart the router."
            ])

    if not problems:

        primary = "Your network appears healthy."

        recommendations = [
            "No major network problems were detected.",
            "Continue monitoring your network if problems appear later."
        ]

    else:

        primary = problems[0]

    recommendations = list(
        dict.fromkeys(recommendations)
    )

    return {
        "primary": primary,
        "problems": problems,
        "recommendations": recommendations
    }