import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import json
from datetime import datetime

from network.connectivity import check_internet
from network.ping_test import ping_host
from network.dns_test import dns_test
from network.gateway import get_gateway, ping_gateway
from network.tcp_test import tcp_test

from diagnosis.engine import calculate_score, generate_diagnosis


class NetworkDoctor:

    def __init__(self, root):

        self.root = root
        self.root.title("Network Doctor")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.results = None

        self.setup_gui()

    # --------------------------------------------------
    # GUI
    # --------------------------------------------------

    def setup_gui(self):

        tk.Label(
            self.root,
            text="🩺 NETWORK DOCTOR",
            font=("Arial", 28, "bold")
        ).pack(pady=(25, 5))

        tk.Label(
            self.root,
            text="Diagnose Your Network Like a Doctor",
            font=("Arial", 13)
        ).pack()

        # Health score
        score_frame = tk.Frame(
            self.root,
            bd=2,
            relief="groove",
            padx=30,
            pady=15
        )

        score_frame.pack(pady=20)

        tk.Label(
            score_frame,
            text="NETWORK HEALTH",
            font=("Arial", 12, "bold")
        ).pack()

        self.health_score = tk.Label(
            score_frame,
            text="-- / 100",
            font=("Arial", 30, "bold")
        )

        self.health_score.pack()

        self.health_status = tk.Label(
            score_frame,
            text="Run diagnosis to check your network",
            font=("Arial", 11)
        )

        self.health_status.pack()

        # Test cards
        self.internet_label = self.create_card(
            "Internet",
            "Not tested"
        )

        self.latency_label = self.create_card(
            "Latency",
            "Not tested"
        )

        self.packet_label = self.create_card(
            "Packet Loss",
            "Not tested"
        )

        self.dns_label = self.create_card(
            "DNS",
            "Not tested"
        )

        self.gateway_label = self.create_card(
            "Gateway",
            "Not tested"
        )

        self.tcp_label = self.create_card(
            "TCP",
            "Not tested"
        )

        # Progress
        self.progress_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 10)
        )

        self.progress_label.pack(pady=(10, 5))

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        self.start_button = tk.Button(
            button_frame,
            text="START DIAGNOSIS",
            font=("Arial", 13, "bold"),
            padx=25,
            pady=10,
            command=self.start_diagnosis
        )

        self.start_button.grid(
            row=0,
            column=0,
            padx=5
        )

        self.save_button = tk.Button(
            button_frame,
            text="SAVE REPORT",
            font=("Arial", 11),
            padx=20,
            pady=10,
            command=self.save_report,
            state="disabled"
        )

        self.save_button.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            self.root,
            text="Computer Networks Engineering Project",
            font=("Arial", 9)
        ).pack(
            side="bottom",
            pady=10
        )

    def create_card(self, title, value):

        frame = tk.Frame(self.root)
        frame.pack(pady=2)

        label = tk.Label(
            frame,
            text=f"{title}: {value}",
            font=("Arial", 11),
            width=50,
            anchor="w"
        )

        label.pack()

        return label

    # --------------------------------------------------
    # Start diagnosis
    # --------------------------------------------------

    def start_diagnosis(self):

        self.start_button.config(
            state="disabled"
        )

        self.save_button.config(
            state="disabled"
        )

        self.health_score.config(
            text="..."
        )

        self.health_status.config(
            text="Running diagnostics..."
        )

        thread = threading.Thread(
            target=self.run_diagnosis,
            daemon=True
        )

        thread.start()

    # --------------------------------------------------
    # Progress
    # --------------------------------------------------

    def update_progress(self, message):

        self.root.after(
            0,
            lambda: self.progress_label.config(
                text=message
            )
        )

    # --------------------------------------------------
    # Run tests
    # --------------------------------------------------

    def run_diagnosis(self):

        results = {}

        # Internet
        self.update_progress(
            "Testing internet connectivity..."
        )

        results["internet"] = check_internet()

        # Ping
        self.update_progress(
            "Testing latency and packet loss..."
        )

        results["ping"] = ping_host(
            "8.8.8.8",
            5
        )

        # DNS
        self.update_progress(
            "Testing DNS resolution..."
        )

        results["dns"] = dns_test(
            "example.com"
        )

        # Gateway
        self.update_progress(
            "Detecting default gateway..."
        )

        gateway = get_gateway()

        results["gateway"] = gateway

        self.update_progress(
            "Testing gateway..."
        )

        results["gateway_latency"] = ping_gateway(
            gateway
        )

        # TCP
        self.update_progress(
            "Testing TCP connectivity..."
        )

        results["tcp"] = {

            "HTTPS": tcp_test(
                "google.com",
                443
            ),

            "DNS": tcp_test(
                "8.8.8.8",
                53
            )
        }

        # Basic interface information
        results["interface"] = {
            "hostname": self.root.winfo_toplevel().title(),
            "local_ip": "Detected by network tests"
        }

        # Score
        self.update_progress(
            "Calculating network health..."
        )

        results["score"] = calculate_score(
            results
        )

        # Diagnosis
        results["diagnosis"] = generate_diagnosis(
            results
        )

        self.results = results

        self.root.after(
            0,
            self.display_results
        )

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------

    def display_results(self):

        results = self.results

        score = results["score"]

        self.health_score.config(
            text=f"{score} / 100"
        )

        if score >= 80:
            status = "EXCELLENT 🟢"

        elif score >= 60:
            status = "GOOD 🟢"

        elif score >= 40:
            status = "FAIR 🟡"

        else:
            status = "POOR 🔴"

        self.health_status.config(
            text=status
        )

        # Internet
        if results["internet"]["status"]:

            self.internet_label.config(
                text="Internet: CONNECTED ✓"
            )

        else:

            self.internet_label.config(
                text="Internet: DISCONNECTED ✗"
            )

        # Latency
        average = results["ping"].get(
            "average"
        )

        self.latency_label.config(
            text=(
                f"Latency: {average} ms"
                if average is not None
                else "Latency: Unavailable"
            )
        )

        # Packet loss
        loss = results["ping"].get(
            "packet_loss"
        )

        self.packet_label.config(
            text=(
                f"Packet Loss: {loss}%"
                if loss is not None
                else "Packet Loss: Unavailable"
            )
        )

        # DNS
        dns_time = results["dns"].get(
            "time"
        )

        self.dns_label.config(
            text=(
                f"DNS: {dns_time} ms"
                if dns_time is not None
                else "DNS: Unavailable"
            )
        )

        # Gateway
        gateway = results["gateway"]
        gateway_latency = results["gateway_latency"]

        if gateway_latency is not None:

            self.gateway_label.config(
                text=(
                    f"Gateway: {gateway} "
                    f"({gateway_latency} ms)"
                )
            )

        else:

            self.gateway_label.config(
                text=f"Gateway: {gateway}"
            )

        # TCP
        tcp_results = results["tcp"]

        tcp_ok = sum(
            1
            for test in tcp_results.values()
            if test["success"]
        )

        self.tcp_label.config(
            text=f"TCP Services: {tcp_ok}/2 reachable"
        )

        self.progress_label.config(
            text="Diagnosis complete ✓"
        )

        self.start_button.config(
            state="normal"
        )

        self.save_button.config(
            state="normal"
        )

        self.show_diagnosis()

    # --------------------------------------------------
    # Diagnosis window
    # --------------------------------------------------

    def show_diagnosis(self):

        diagnosis = self.results["diagnosis"]

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Network Diagnosis"
        )

        window.geometry(
            "650x600"
        )

        tk.Label(
            window,
            text="🩺 NETWORK DIAGNOSIS",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            window,
            text=diagnosis["primary"],
            font=("Arial", 14, "bold"),
            wraplength=550
        ).pack(pady=10)

        tk.Label(
            window,
            text="Detected Issues",
            font=("Arial", 13, "bold")
        ).pack(pady=(20, 5))

        if diagnosis["problems"]:

            for problem in diagnosis["problems"]:

                tk.Label(
                    window,
                    text="• " + problem,
                    font=("Arial", 11),
                    wraplength=550,
                    justify="left"
                ).pack(
                    anchor="w",
                    padx=50,
                    pady=2
                )

        else:

            tk.Label(
                window,
                text="✓ No major problems detected.",
                font=("Arial", 11)
            ).pack()

        tk.Label(
            window,
            text="Recommendations",
            font=("Arial", 13, "bold")
        ).pack(pady=(25, 5))

        for recommendation in diagnosis[
            "recommendations"
        ]:

            tk.Label(
                window,
                text="✓ " + recommendation,
                font=("Arial", 11),
                wraplength=550,
                justify="left"
            ).pack(
                anchor="w",
                padx=50,
                pady=2
            )

    # --------------------------------------------------
    # Save report
    # --------------------------------------------------

    def save_report(self):

        if not self.results:
            return

        filename = filedialog.asksaveasfilename(

            defaultextension=".json",

            filetypes=[
                ("JSON Report", "*.json"),
                ("Text Report", "*.txt")
            ],

            initialfile="network_doctor_report"
        )

        if not filename:
            return

        try:

            if filename.endswith(".json"):

                with open(
                    filename,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        self.results,
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
                        self.create_text_report()
                    )

            messagebox.showinfo(
                "Network Doctor",
                "Report saved successfully! ✓"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not save report:\n{error}"
            )

    def create_text_report(self):

        results = self.results
        diagnosis = results["diagnosis"]

        report = []

        report.append(
            "===================================="
        )

        report.append(
            "        NETWORK DOCTOR REPORT"
        )

        report.append(
            "===================================="
        )

        report.append(
            f"Generated: {datetime.now()}"
        )

        report.append("")

        report.append(
            f"Health Score: {results['score']}/100"
        )

        report.append("")

        report.append("NETWORK TESTS")
        report.append("------------------------------------")

        report.append(
            f"Internet: {results['internet']['status']}"
        )

        report.append(
            f"Average Latency: "
            f"{results['ping'].get('average')} ms"
        )

        report.append(
            f"Packet Loss: "
            f"{results['ping'].get('packet_loss')}%"
        )

        report.append(
            f"DNS Response: "
            f"{results['dns'].get('time')} ms"
        )

        report.append(
            f"Gateway: {results['gateway']}"
        )

        report.append(
            f"Gateway Latency: "
            f"{results['gateway_latency']} ms"
        )

        report.append("")

        report.append("DIAGNOSIS")
        report.append("------------------------------------")

        report.append(
            diagnosis["primary"]
        )

        report.append("")

        report.append("PROBLEMS")

        for problem in diagnosis["problems"]:
            report.append(
                "- " + problem
            )

        report.append("")

        report.append("RECOMMENDATIONS")

        for recommendation in diagnosis[
            "recommendations"
        ]:

            report.append(
                "- " + recommendation
            )

        return "\n".join(report)


# --------------------------------------------------
# APPLICATION START
# --------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = NetworkDoctor(root)

    root.mainloop()