import tkinter as tk
from tkinter import messagebox, filedialog
import socket
import subprocess
import platform
import time
import threading
import json
import re
from datetime import datetime


# ============================================================
# COLORS / THEME
# ============================================================

BG = "#0F172A"
CARD = "#1E293B"
CARD_LIGHT = "#263449"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
GREEN = "#22C55E"
RED = "#EF4444"
YELLOW = "#F59E0B"
BLUE = "#38BDF8"
PURPLE = "#A78BFA"
WHITE = "#FFFFFF"


# ============================================================
# NETWORK TEST FUNCTIONS
# ============================================================

def check_internet():
    try:
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )
        return True
    except Exception:
        return False


def ping_host(host="8.8.8.8"):
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-4", "-n", "4", host]
    else:
        command = ["ping", "-4", "-c", "4", host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout

        loss_match = re.search(
            r"(\d+(?:\.\d+)?)%\s*(?:loss|packet loss)",
            output,
            re.IGNORECASE
        )

        packet_loss = (
            float(loss_match.group(1))
            if loss_match else None
        )

        latency = None

        if system == "windows":

            avg_match = re.search(
                r"Average\s*=\s*(\d+)ms",
                output,
                re.IGNORECASE
            )

            if avg_match:
                latency = float(
                    avg_match.group(1)
                )

        else:

            avg_match = re.search(
                r"=\s*[\d.]+/([\d.]+)/",
                output
            )

            if avg_match:
                latency = float(
                    avg_match.group(1)
                )

        return {
            "latency": latency,
            "packet_loss": packet_loss,
            "raw_output": output
        }

    except Exception as e:

        return {
            "latency": None,
            "packet_loss": None,
            "raw_output": str(e)
        }


def dns_test():

    start = time.time()

    try:

        socket.gethostbyname(
            "google.com"
        )

        elapsed = round(
            (time.time() - start) * 1000,
            2
        )

        return {
            "status": True,
            "response_time": elapsed
        }

    except Exception:

        return {
            "status": False,
            "response_time": None
        }


def get_local_ip():

    try:

        hostname = socket.gethostname()

        ip = socket.gethostbyname(
            hostname
        )

        if not ip.startswith("127."):

            return ip

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        sock.connect(
            ("8.8.8.8", 80)
        )

        ip = sock.getsockname()[0]

        sock.close()

        return ip

    except Exception:

        return "Unavailable"


def get_gateway():

    system = platform.system().lower()

    try:

        if system == "windows":

            result = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
                timeout=10
            )

            for line in result.stdout.splitlines():

                if "Default Gateway" in line:

                    parts = line.split(":")

                    if len(parts) > 1:

                        gateway = parts[1].strip()

                        if gateway:
                            return gateway

        else:

            result = subprocess.run(
                ["ip", "route"],
                capture_output=True,
                text=True,
                timeout=10
            )

            match = re.search(
                r"default via ([0-9.]+)",
                result.stdout
            )

            if match:
                return match.group(1)

    except Exception:
        pass

    return "Unavailable"


def gateway_ping(gateway):

    if gateway == "Unavailable":

        return {
            "status": False,
            "latency": None
        }

    result = ping_host(
        gateway
    )

    return {
        "status": result["latency"] is not None,
        "latency": result["latency"]
    }


def tcp_test(
    host="google.com",
    port=443
):

    try:

        start = time.time()

        sock = socket.create_connection(
            (host, port),
            timeout=5
        )

        sock.close()

        elapsed = round(
            (time.time() - start) * 1000,
            2
        )

        return {
            "status": True,
            "response_time": elapsed
        }

    except Exception:

        return {
            "status": False,
            "response_time": None
        }


def get_interface_info():

    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "local_ip": get_local_ip(),
        "gateway": get_gateway()
    }


# ============================================================
# TRACEROUTE
# ============================================================

def traceroute(host="8.8.8.8"):

    system = platform.system().lower()

    try:

        if system == "windows":

            command = [
                "tracert",
                "-4",
                "-d",
                "-h",
                "12",
                host
            ]

        else:

            command = [
                "traceroute",
                "-4",
                "-m",
                "12",
                host
            ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout

        if not output:
            output = result.stderr

        return output

    except FileNotFoundError:

        return (
            "Traceroute command is not available "
            "on this system."
        )

    except subprocess.TimeoutExpired:

        return "Traceroute timed out."

    except Exception as e:

        return f"Traceroute error: {e}"


# ============================================================
# SCORING
# ============================================================

def latency_score(latency):

    if latency is None:
        return 0

    if latency <= 30:
        return 20
    elif latency <= 60:
        return 17
    elif latency <= 100:
        return 14
    elif latency <= 150:
        return 10
    elif latency <= 250:
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
        return 12
    elif loss <= 10:
        return 7

    return 2


def dns_score(result):

    if not result["status"]:
        return 0

    response_time = result["response_time"]

    if response_time <= 50:
        return 15
    elif response_time <= 100:
        return 12
    elif response_time <= 200:
        return 9

    return 5


def calculate_score(results):

    score = 0

    if results["internet"]:
        score += 20

    score += latency_score(
        results["ping"]["latency"]
    )

    score += packet_loss_score(
        results["ping"]["packet_loss"]
    )

    score += dns_score(
        results["dns"]
    )

    if results["gateway"]["status"]:
        score += 10

    if results["tcp"]["status"]:
        score += 10

    if results["interface"]["local_ip"] != "Unavailable":
        score += 5

    return score


# ============================================================
# DIAGNOSIS
# ============================================================

def generate_diagnosis(results):

    problems = []
    causes = []
    recommendations = []

    if not results["internet"]:

        problems.append(
            "Internet connectivity is unavailable."
        )

        causes.append(
            "The device may be disconnected "
            "from the network."
        )

        recommendations.append(
            "Check Wi-Fi/Ethernet connection "
            "and router status."
        )

    latency = results["ping"]["latency"]

    if latency is not None and latency > 100:

        problems.append(
            "High network latency detected."
        )

        causes.append(
            "The connection may be congested "
            "or the destination may be far away."
        )

        recommendations.append(
            "Try reducing network traffic "
            "or moving closer to the router."
        )

    loss = results["ping"]["packet_loss"]

    if loss is not None and loss > 2:

        problems.append(
            "Packet loss detected."
        )

        causes.append(
            "Packets may be getting dropped "
            "between the device and destination."
        )

        recommendations.append(
            "Check Wi-Fi signal strength, "
            "cables and router stability."
        )

    if not results["dns"]["status"]:

        problems.append(
            "DNS resolution failed."
        )

        causes.append(
            "The DNS server may be unavailable."
        )

        recommendations.append(
            "Try a reliable DNS server such "
            "as Google DNS or Cloudflare DNS."
        )

    if not results["gateway"]["status"]:

        problems.append(
            "Default gateway is not responding."
        )

        causes.append(
            "The local router or gateway "
            "may be unreachable."
        )

        recommendations.append(
            "Check the router and local "
            "network configuration."
        )

    if not results["tcp"]["status"]:

        problems.append(
            "TCP connection test failed."
        )

        causes.append(
            "The service may be unreachable "
            "or blocked by a firewall."
        )

        recommendations.append(
            "Check firewall settings and "
            "test another network service."
        )

    if not problems:

        problems.append(
            "No major network problems detected."
        )

        causes.append(
            "All diagnostic tests completed successfully."
        )

        recommendations.append(
            "Your network appears healthy."
        )

    return {
        "problems": problems,
        "causes": causes,
        "recommendations": recommendations
    }


# ============================================================
# APPLICATION
# ============================================================

class NetworkDoctor:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Network Doctor"
        )

        self.root.geometry(
            "900x760"
        )

        self.root.configure(
            bg=BG
        )

        self.root.resizable(
            False,
            False
        )

        self.results = None

        self.setup_gui()


    # ========================================================
    # GUI
    # ========================================================

    def setup_gui(self):

        # ---------- HEADER ----------

        header = tk.Frame(
            self.root,
            bg=BG
        )

        header.pack(
            fill="x",
            pady=(25, 5)
        )

        tk.Label(
            header,
            text="🩺",
            font=("Segoe UI Emoji", 32),
            bg=BG,
            fg=WHITE
        ).pack()

        tk.Label(
            header,
            text="NETWORK DOCTOR",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=WHITE
        ).pack()

        tk.Label(
            header,
            text="Diagnose your network like a doctor",
            font=("Segoe UI", 11),
            bg=BG,
            fg=MUTED
        ).pack(
            pady=(2, 10)
        )


        # ---------- STATUS ----------

        self.status_card = tk.Frame(
            self.root,
            bg=CARD,
            height=65
        )

        self.status_card.pack(
            fill="x",
            padx=35,
            pady=10
        )

        self.status_card.pack_propagate(
            False
        )

        self.status_label = tk.Label(
            self.status_card,
            text="●  INTERNET STATUS: NOT TESTED",
            font=("Segoe UI", 12, "bold"),
            bg=CARD,
            fg=MUTED
        )

        self.status_label.pack(
            pady=20
        )


        # ---------- SCORE ----------

        score_frame = tk.Frame(
            self.root,
            bg=CARD
        )

        score_frame.pack(
            fill="x",
            padx=35,
            pady=8
        )

        tk.Label(
            score_frame,
            text="NETWORK HEALTH",
            font=("Segoe UI", 10, "bold"),
            bg=CARD,
            fg=MUTED
        ).pack(
            pady=(18, 0)
        )

        self.score_label = tk.Label(
            score_frame,
            text="-- / 100",
            font=("Segoe UI", 34, "bold"),
            bg=CARD,
            fg=WHITE
        )

        self.score_label.pack(
            pady=2
        )

        self.rating_label = tk.Label(
            score_frame,
            text="Run a diagnosis to calculate your score",
            font=("Segoe UI", 11),
            bg=CARD,
            fg=MUTED
        )

        self.rating_label.pack(
            pady=(0, 18)
        )


        # ---------- TEST CARDS ----------

        tests_frame = tk.Frame(
            self.root,
            bg=BG
        )

        tests_frame.pack(
            padx=35,
            pady=10
        )


        self.test_labels = {}

        tests = [
            ("Internet", "🌐"),
            ("Latency", "⚡"),
            ("Packet Loss", "📦"),
            ("DNS", "🔎"),
            ("Gateway", "🚪"),
            ("TCP Services", "🔗")
        ]


        for index, (name, icon) in enumerate(tests):

            row = index // 3
            col = index % 3

            card = tk.Frame(
                tests_frame,
                bg=CARD_LIGHT,
                width=250,
                height=70
            )

            card.grid(
                row=row,
                column=col,
                padx=6,
                pady=6
            )

            card.grid_propagate(
                False
            )


            tk.Label(
                card,
                text=icon,
                font=("Segoe UI Emoji", 16),
                bg=CARD_LIGHT,
                fg=WHITE
            ).pack(
                side="left",
                padx=(12, 7)
            )


            text_label = tk.Label(
                card,
                text=f"{name}\nNot tested",
                font=("Segoe UI", 10, "bold"),
                bg=CARD_LIGHT,
                fg=WHITE,
                justify="left"
            )

            text_label.pack(
                side="left"
            )

            self.test_labels[name] = text_label


        # ---------- BUTTONS ----------

        button_frame = tk.Frame(
            self.root,
            bg=BG
        )

        button_frame.pack(
            pady=12
        )


        self.start_button = tk.Button(
            button_frame,
            text="🩺  START DIAGNOSIS",
            font=("Segoe UI", 11, "bold"),
            bg=BLUE,
            fg="#0F172A",
            activebackground="#7DD3FC",
            relief="flat",
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.start_diagnosis
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=5
        )


        self.info_button = tk.Button(
            button_frame,
            text="🌐  NETWORK INFO",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_LIGHT,
            fg=WHITE,
            activebackground=CARD,
            activeforeground=WHITE,
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.show_network_info
        )

        self.info_button.grid(
            row=0,
            column=1,
            padx=5
        )


        self.trace_button = tk.Button(
            button_frame,
            text="🛣  TRACEROUTE",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_LIGHT,
            fg=WHITE,
            activebackground=CARD,
            activeforeground=WHITE,
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.run_traceroute
        )

        self.trace_button.grid(
            row=0,
            column=2,
            padx=5
        )


        # ---------- SECOND BUTTON ROW ----------

        second_buttons = tk.Frame(
            self.root,
            bg=BG
        )

        second_buttons.pack(
            pady=3
        )


        self.diagnosis_button = tk.Button(
            second_buttons,
            text="🔍  VIEW DIAGNOSIS",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_LIGHT,
            fg=WHITE,
            activebackground=CARD,
            activeforeground=WHITE,
            relief="flat",
            padx=22,
            pady=8,
            cursor="hand2",
            command=self.show_diagnosis,
            state="disabled"
        )

        self.diagnosis_button.grid(
            row=0,
            column=0,
            padx=5
        )


        self.save_button = tk.Button(
            second_buttons,
            text="💾  SAVE REPORT",
            font=("Segoe UI", 10, "bold"),
            bg=CARD_LIGHT,
            fg=WHITE,
            activebackground=CARD,
            activeforeground=WHITE,
            relief="flat",
            padx=22,
            pady=8,
            cursor="hand2",
            command=self.save_report,
            state="disabled"
        )

        self.save_button.grid(
            row=0,
            column=1,
            padx=5
        )


        # ---------- PROGRESS ----------

        self.progress_label = tk.Label(
            self.root,
            text="Ready to diagnose your network.",
            font=("Segoe UI", 9),
            bg=BG,
            fg=MUTED
        )

        self.progress_label.pack(
            pady=15
        )


    # ========================================================
    # DIAGNOSIS
    # ========================================================

    def start_diagnosis(self):

        self.start_button.config(
            state="disabled"
        )

        self.info_button.config(
            state="disabled"
        )

        self.trace_button.config(
            state="disabled"
        )

        self.diagnosis_button.config(
            state="disabled"
        )

        self.save_button.config(
            state="disabled"
        )

        self.progress_label.config(
            text="Running network diagnostics..."
        )


        thread = threading.Thread(
            target=self.run_diagnosis,
            daemon=True
        )

        thread.start()


    def run_diagnosis(self):

        results = {}


        self.update_progress(
            "Checking internet connectivity..."
        )

        results["internet"] = check_internet()


        self.update_progress(
            "Measuring latency and packet loss..."
        )

        results["ping"] = ping_host()


        self.update_progress(
            "Testing DNS resolution..."
        )

        results["dns"] = dns_test()


        self.update_progress(
            "Checking default gateway..."
        )

        gateway = get_gateway()

        results["gateway"] = gateway_ping(
            gateway
        )


        self.update_progress(
            "Testing TCP connectivity..."
        )

        results["tcp"] = tcp_test()


        self.update_progress(
            "Collecting network information..."
        )

        results["interface"] = (
            get_interface_info()
        )


        results["score"] = calculate_score(
            results
        )


        results["diagnosis"] = (
            generate_diagnosis(
                results
            )
        )


        self.results = results


        self.root.after(
            0,
            self.display_results
        )


    def update_progress(self, text):

        self.root.after(
            0,
            lambda: self.progress_label.config(
                text=text
            )
        )


    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    def display_results(self):

        results = self.results


        # Internet
        if results["internet"]:

            self.test_labels[
                "Internet"
            ].config(
                text="Internet\nConnected",
                fg=GREEN
            )

            self.status_label.config(
                text="●  INTERNET STATUS: CONNECTED",
                fg=GREEN
            )

        else:

            self.test_labels[
                "Internet"
            ].config(
                text="Internet\nDisconnected",
                fg=RED
            )

            self.status_label.config(
                text="●  INTERNET STATUS: DISCONNECTED",
                fg=RED
            )


        # Latency
        latency = results["ping"]["latency"]

        if latency is not None:

            self.test_labels[
                "Latency"
            ].config(
                text=f"Latency\n{latency} ms",
                fg=GREEN if latency <= 100 else YELLOW
            )

        else:

            self.test_labels[
                "Latency"
            ].config(
                text="Latency\nUnavailable",
                fg=RED
            )


        # Packet loss
        loss = results["ping"]["packet_loss"]

        if loss is not None:

            self.test_labels[
                "Packet Loss"
            ].config(
                text=f"Packet Loss\n{loss}%",
                fg=GREEN if loss <= 2 else YELLOW
            )

        else:

            self.test_labels[
                "Packet Loss"
            ].config(
                text="Packet Loss\nUnavailable",
                fg=RED
            )


        # DNS
        if results["dns"]["status"]:

            self.test_labels[
                "DNS"
            ].config(
                text=(
                    f"DNS\n"
                    f"{results['dns']['response_time']} ms"
                ),
                fg=GREEN
            )

        else:

            self.test_labels[
                "DNS"
            ].config(
                text="DNS\nFailed",
                fg=RED
            )


        # Gateway
        if results["gateway"]["status"]:

            self.test_labels[
                "Gateway"
            ].config(
                text="Gateway\nReachable",
                fg=GREEN
            )

        else:

            self.test_labels[
                "Gateway"
            ].config(
                text="Gateway\nUnavailable",
                fg=RED
            )


        # TCP
        if results["tcp"]["status"]:

            self.test_labels[
                "TCP Services"
            ].config(
                text=(
                    f"TCP Services\n"
                    f"Connected"
                ),
                fg=GREEN
            )

        else:

            self.test_labels[
                "TCP Services"
            ].config(
                text="TCP Services\nFailed",
                fg=RED
            )


        # Score
        score = results["score"]


        if score >= 80:

            rating = "EXCELLENT"
            score_color = GREEN

        elif score >= 60:

            rating = "GOOD"
            score_color = BLUE

        elif score >= 40:

            rating = "FAIR"
            score_color = YELLOW

        else:

            rating = "POOR"
            score_color = RED


        self.score_label.config(
            text=f"{score} / 100",
            fg=score_color
        )


        self.rating_label.config(
            text=rating,
            fg=score_color
        )


        self.progress_label.config(
            text="✓ Diagnosis completed successfully."
        )


        self.start_button.config(
            state="normal"
        )

        self.info_button.config(
            state="normal"
        )

        self.trace_button.config(
            state="normal"
        )

        self.diagnosis_button.config(
            state="normal"
        )

        self.save_button.config(
            state="normal"
        )


    # ========================================================
    # NETWORK INFORMATION
    # ========================================================

    def show_network_info(self):

        info = get_interface_info()


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Network Information"
        )

        window.geometry(
            "560x400"
        )

        window.configure(
            bg=BG
        )


        tk.Label(
            window,
            text="🌐  NETWORK INFORMATION",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            pady=25
        )


        details = [
            ("Hostname", info["hostname"]),
            ("Operating System", info["operating_system"]),
            ("Local IPv4", info["local_ip"]),
            ("Default Gateway", info["gateway"])
        ]


        for name, value in details:

            card = tk.Frame(
                window,
                bg=CARD_LIGHT
            )

            card.pack(
                fill="x",
                padx=45,
                pady=6
            )


            tk.Label(
                card,
                text=name,
                font=("Segoe UI", 10, "bold"),
                bg=CARD_LIGHT,
                fg=MUTED,
                width=20,
                anchor="w"
            ).pack(
                side="left",
                padx=15,
                pady=12
            )


            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 10),
                bg=CARD_LIGHT,
                fg=WHITE,
                anchor="w"
            ).pack(
                side="left",
                padx=10
            )


    # ========================================================
    # TRACEROUTE
    # ========================================================

    def run_traceroute(self):

        self.trace_button.config(
            state="disabled"
        )


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "IPv4 Network Traceroute"
        )

        window.geometry(
            "800x570"
        )

        window.configure(
            bg=BG
        )


        tk.Label(
            window,
            text="🛣  NETWORK TRACEROUTE",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            pady=(20, 5)
        )


        tk.Label(
            window,
            text=(
                "Tracing IPv4 route to Google's public DNS "
                "server — 8.8.8.8"
            ),
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        ).pack(
            pady=(0, 15)
        )


        text_box = tk.Text(
            window,
            font=("Consolas", 10),
            bg="#020617",
            fg="#CBD5E1",
            insertbackground=WHITE,
            relief="flat",
            padx=15,
            pady=15
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        text_box.insert(
            "end",
            "Starting IPv4 traceroute...\n\n"
        )


        def worker():

            output = traceroute(
                "8.8.8.8"
            )

            self.root.after(
                0,
                lambda: finish(output)
            )


        def finish(output):

            text_box.delete(
                "1.0",
                "end"
            )

            text_box.insert(
                "end",
                output
            )

            self.trace_button.config(
                state="normal"
            )


        threading.Thread(
            target=worker,
            daemon=True
        ).start()


    # ========================================================
    # DIAGNOSIS WINDOW
    # ========================================================

    def show_diagnosis(self):

        if not self.results:
            return


        diagnosis = self.results[
            "diagnosis"
        ]


        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Network Diagnosis"
        )

        window.geometry(
            "700x650"
        )

        window.configure(
            bg=BG
        )


        tk.Label(
            window,
            text="🩺  NETWORK DIAGNOSIS",
            font=("Segoe UI", 22, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            pady=20
        )


        sections = [
            (
                "Problems Detected",
                diagnosis["problems"],
                RED
            ),
            (
                "Possible Causes",
                diagnosis["causes"],
                YELLOW
            ),
            (
                "Recommended Actions",
                diagnosis["recommendations"],
                GREEN
            )
        ]


        for title, items, color in sections:

            tk.Label(
                window,
                text=title,
                font=("Segoe UI", 13, "bold"),
                bg=BG,
                fg=color
            ).pack(
                anchor="w",
                padx=35,
                pady=(12, 5)
            )


            for item in items:

                tk.Label(
                    window,
                    text="• " + item,
                    font=("Segoe UI", 10),
                    bg=BG,
                    fg=TEXT,
                    wraplength=620,
                    justify="left"
                ).pack(
                    anchor="w",
                    padx=50,
                    pady=4
                )


    # ========================================================
    # SAVE REPORT
    # ========================================================

    def save_report(self):

        if not self.results:
            return


        filename = filedialog.asksaveasfilename(
            title="Save Network Report",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt")
            ]
        )


        if not filename:
            return


        report = {
            "application": "Network Doctor",
            "generated_at": datetime.now().isoformat(),
            "results": self.results
        }


        try:

            if filename.endswith(".json"):

                with open(
                    filename,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        report,
                        file,
                        indent=4
                    )

            else:

                with open(
                    filename,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        "NETWORK DOCTOR REPORT\n"
                    )

                    file.write(
                        "=" * 55 + "\n\n"
                    )

                    file.write(
                        f"Generated: "
                        f"{report['generated_at']}\n\n"
                    )

                    file.write(
                        f"Network Health: "
                        f"{self.results['score']}/100\n\n"
                    )

                    file.write(
                        f"Internet: "
                        f"{self.results['internet']}\n"
                    )

                    file.write(
                        f"Latency: "
                        f"{self.results['ping']['latency']} ms\n"
                    )

                    file.write(
                        f"Packet Loss: "
                        f"{self.results['ping']['packet_loss']}%\n"
                    )

                    file.write(
                        f"DNS: "
                        f"{self.results['dns']['status']}\n"
                    )

                    file.write(
                        f"Gateway: "
                        f"{self.results['interface']['gateway']}\n"
                    )

                    file.write(
                        f"Local IP: "
                        f"{self.results['interface']['local_ip']}\n"
                    )


            messagebox.showinfo(
                "Report Saved",
                "Your network diagnostic report "
                "was saved successfully."
            )


        except Exception as e:

            messagebox.showerror(
                "Save Error",
                f"Could not save report:\n{e}"
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = NetworkDoctor(
        root
    )

    root.mainloop()