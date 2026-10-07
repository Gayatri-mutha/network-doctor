# 🩺 Network Doctor

### Diagnose Your Network Like a Doctor

Network Doctor is a real-time desktop network diagnostic application developed using Python. It performs multiple network tests, evaluates the results, calculates a **Network Health Score**, and provides a simple diagnosis with recommended actions.

The project is designed as a **Computer Networks academic project** and demonstrates practical concepts such as connectivity, latency, packet loss, DNS, gateways, TCP connections, and network routing.

---

## 🎯 Problem Statement

When an internet connection becomes slow or unstable, users often do not know what is causing the problem.

The problem could be:

- High latency
- Packet loss
- DNS failure
- Gateway problems
- TCP connectivity issues
- Local network configuration problems

Network Doctor provides a single interface that performs these diagnostic tests and explains the results in a user-friendly way.

---

## 💡 Solution

Network Doctor acts like a **doctor for your network**.

It:

1. Checks whether the internet is reachable.
2. Measures network latency.
3. Detects packet loss.
4. Tests DNS resolution.
5. Checks the default gateway.
6. Tests TCP connectivity.
7. Collects local network information.
8. Performs IPv4 traceroute.
9. Calculates a Network Health Score.
10. Generates a rule-based diagnosis.
11. Allows the user to save a diagnostic report.

---

## ✨ Features

### 🩺 Network Diagnosis

Runs multiple real network tests and combines their results into one health assessment.

### 📊 Network Health Score

The application calculates a score out of 100.

| Component | Maximum Score |
|---|---:|
| Internet Connectivity | 20 |
| Latency | 20 |
| Packet Loss | 20 |
| DNS | 15 |
| Gateway | 10 |
| TCP Connectivity | 10 |
| Network Interface | 5 |
| **Total** | **100** |

### ⚡ Latency Test

Measures the response time between the local machine and a network destination.

### 📦 Packet Loss Detection

Checks whether packets are being lost during communication.

### 🔎 DNS Test

Tests whether domain-name resolution is functioning correctly.

### 🚪 Gateway Test

Detects and tests the default network gateway.

### 🔗 TCP Connectivity

Tests whether a TCP connection can be established with a network service.

### 🌐 Network Information

Displays:

- Hostname
- Operating system
- Local IPv4 address
- Default gateway

### 🛣️ IPv4 Traceroute

Uses the operating system's traceroute functionality to display the network hops between the computer and Google's public DNS server (`8.8.8.8`).

### 🔍 Automatic Diagnosis

The application analyzes the test results and provides:

- Problems detected
- Possible causes
- Recommended actions

### 💾 Report Generation

Diagnostic results can be saved as:

- JSON
- TXT

---

## 🧠 Computer Networks Concepts Used

This project connects theoretical Computer Networks concepts with practical implementation.

### 1. IP Addressing

The application identifies the local IPv4 address of the host machine.

### 2. DNS

The DNS test demonstrates how domain names such as `google.com` are resolved into IP addresses.

### 3. ICMP / Ping

Ping is used to measure network response time and packet loss.

### 4. Default Gateway

The application detects the gateway through which the local machine communicates with external networks.

### 5. TCP

The application establishes a TCP connection to test service-level connectivity.

### 6. Routing

Traceroute demonstrates how packets travel through multiple network hops before reaching a destination.

### 7. Network Diagnostics

Multiple measurements are combined to evaluate the overall condition of the network.

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │    Network Doctor    │
                 │         GUI         │
                 └──────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       Network Tests                 User Actions
              │                           │
     ┌────────┼────────┐          ┌───────┼────────┐
     │        │        │          │       │        │
 Internet   Ping     DNS       Diagnosis Report  Traceroute
     │        │        │          │       │        │
     └────────┴────────┴──────────┴───────┴────────┘
                            │
                    ┌───────▼────────┐
                    │ Health Scoring │
                    │   0 - 100      │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │    Diagnosis   │
                    └────────────────┘
```

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter**
- Python Socket Library
- Python Subprocess Library
- Python Threading
- JSON
- Regular Expressions
- Windows networking utilities

No external networking framework is required for the core application.

---

## 📁 Project Structure

```text
network-doctor/
│
├── app.py
├── app_backup.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── gui/
│   └── __init__.py
│
├── network/
│   ├── __init__.py
│   ├── connectivity.py
│   ├── ping_test.py
│   ├── dns_test.py
│   ├── gateway.py
│   └── tcp_test.py
│
├── diagnosis/
│   ├── __init__.py
│   └── engine.py
│
├── reports/
│   ├── __init__.py
│   └── report_generator.py
│
├── utils/
│   └── __init__.py
│
└── tests/
    ├── __init__.py
    └── test_diagnosis.py
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

### 2. Enter the project directory

```bash
cd network-doctor
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 4. Activate the virtual environment

```powershell
venv\Scripts\activate
```

### 5. Run the application

```powershell
python app.py
```

---

## 🖥️ How to Use

### Step 1

Launch the application.

### Step 2

Click:

```text
START DIAGNOSIS
```

### Step 3

The application performs the network tests.

### Step 4

View the calculated:

```text
Network Health Score
```

### Step 5

Use:

```text
NETWORK INFO
```

to view local network information.

### Step 6

Use:

```text
TRACEROUTE
```

to view the route to `8.8.8.8`.

### Step 7

Use:

```text
VIEW DIAGNOSIS
```

to understand possible network problems.

### Step 8

Use:

```text
SAVE REPORT
```

to save the diagnostic results.

---

## 📈 Health Score Interpretation

| Score | Rating |
|---:|---|
| 80–100 | Excellent |
| 60–79 | Good |
| 40–59 | Fair |
| 0–39 | Poor |

The score is calculated from multiple network measurements rather than a single test.

---

## 🔬 Example

A typical diagnosis may produce:

```text
Network Health: 87 / 100

Internet: Connected
Latency: 20 ms
Packet Loss: 0%
DNS: Working
Gateway: Reachable
TCP Services: Connected
```

The exact score can change depending on current network conditions.

---

## 🛡️ Safety

Network Doctor is designed for **diagnostic and educational purposes**.

It does not perform:

- Network exploitation
- Password attacks
- Port scanning of arbitrary systems
- Vulnerability exploitation
- Packet interception
- Unauthorized access

The application only performs basic network connectivity and diagnostic tests.

---

## 🔮 Future Scope

Possible future improvements include:

- Wi-Fi signal strength monitoring
- Historical network health graphs
- Automatic periodic monitoring
- Network speed testing
- More detailed interface statistics
- Exportable PDF reports
- Multi-device monitoring
- Network health notifications
- AI-assisted diagnosis
- Cloud-based monitoring dashboard

---

## 🎓 Academic Relevance

Network Doctor demonstrates how Computer Networks concepts taught in theory can be implemented in a practical application.

The project covers:

**Host → Network Interface → Gateway → Routing → DNS → TCP → Internet**

Instead of studying these concepts independently, the application brings them together into one diagnostic workflow.

---

## 👩‍💻 Project Type

**Academic Project — Computer Networks**

**Application:** Desktop Network Diagnostic Tool

**Language:** Python

**Interface:** Tkinter

**Platform:** Windows / Linux with appropriate networking utilities

---

## 📌 Important Note

Network measurements depend on the current network environment.

Therefore, latency, packet loss, traceroute hops, DNS response time, and the final health score may change between different runs.

This is expected behavior because the application performs **real network diagnostics** rather than using fixed or simulated values.

---

## ⭐ Project Highlights

> **Network Doctor doesn't just tell you whether your internet is working — it investigates why your network may be unhealthy.**

The project combines:

**Real Network Tests + Scoring + Diagnosis + Routing Visualization + Report Generation**

into a single desktop application.