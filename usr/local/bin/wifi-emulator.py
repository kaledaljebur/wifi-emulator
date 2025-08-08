# Created by Kaled Aljebur
# https://github.com/kaledaljebur/wifi-emulator

import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import subprocess
import os
import sys

class WiFi_Emulator:
    def __init__(self, root):
        check_sudo()
        self.root = root
        self.root.title("WiFi Emulator")
        self.root.geometry("800x800")



        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="1. Generate Access Point Conf file", command=self.generate_ap_conf).grid(row=0, column=0, padx=5, sticky="w")
        tk.Button(btn_frame, text="Edit ap.conf", command=lambda: self.edit_conf("ap.conf")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(btn_frame, text="2. Generate Access Client Conf file", command=self.generate_client_conf).grid(row=1, column=0, padx=5, sticky="w")
        tk.Button(btn_frame, text="Edit ac.conf", command=lambda: self.edit_conf("ac.conf")).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Button(btn_frame, text="3. Create Virtual Interfaces", command=self.create_interfaces).grid(row=3, column=0, padx=5, sticky="w")
        tk.Button(btn_frame, text="Edit ap.conf", command=lambda: self.edit_conf("ap.conf")).grid(row=3, column=1, padx=5, pady=5, sticky="w")
        tk.Button(btn_frame, text="4. Start Access Point on wlan0", command=self.start_hostapd).grid(row=4, column=0, padx=5, sticky="w")
        tk.Button(btn_frame, text="Edit ap.conf", command=lambda: self.edit_conf("ap.conf")).grid(row=4, column=1, padx=5, pady=5, sticky="w")
        tk.Button(btn_frame, text="5. Start Start Access Client on wlan1", command=self.start_wpasupplicant).grid(row=5, column=0, padx=5, sticky="w")
        tk.Button(btn_frame, text="Edit ap.conf", command=lambda: self.edit_conf("ap.conf")).grid(row=5, column=1, padx=5, pady=5, sticky="w")
        # tk.Button(btn_frame, text="6. Run Wifite", command=self.run_wifite).grid(row=6, column=0, padx=5, sticky="w")
        tk.Button(btn_frame, text="Help", command=self.start_wpasupplicant).grid(row=7, column=0, padx=5, sticky="w")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
        self.text_area.pack(pady=10)

    def log(self, message):
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.see(tk.END)

    def create_interfaces(self):
        cmd = ["modprobe", "mac80211_hwsim", "radios=3"]
        self.run_cmd(cmd, "Creating 3 virtual Wi-Fi interfaces")

    def generate_ap_conf(self):
        conf = """interface=wlan0
driver=nl80211
ssid=TestAP
channel=6
hw_mode=g
auth_algs=1
wpa=2
wpa_passphrase=sunshine
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP"""
        with open("ap.conf", "w") as f:
            f.write(conf)
        self.log("ap.conf generated")

    def generate_client_conf(self):
        conf = """ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid=\"TestAP\"
    psk=\"sunshine\"
}"""
        with open("ac.conf", "w") as f:
            f.write(conf)
        self.log("ac.conf generated")

    def edit_conf(self, filename):
        editor = tk.Toplevel(self.root)
        editor.title(f"Editing {filename}")

        with open(filename, "r") as f:
            content = f.read()

        text = scrolledtext.ScrolledText(editor, wrap=tk.WORD, width=80, height=20)
        text.pack()
        text.insert(tk.END, content)

        def save_changes():
            with open(filename, "w") as f:
                f.write(text.get("1.0", tk.END))
            self.log(f"{filename} saved")
            editor.destroy()

        tk.Button(editor, text="Save", command=save_changes).pack(pady=5)

    def start_hostapd(self):
        cmd = ["x-terminal-emulator", "-e", "hostapd ap.conf"]
        self.run_cmd(cmd, "Starting hostapd in new terminal")

    def start_wpasupplicant(self):
        cmd = ["x-terminal-emulator", "-e", "wpa_supplicant -i wlan1 -c ac.conf"]
        self.run_cmd(cmd, "Starting wpa_supplicant in new terminal")

    def run_wifite(self):
        cmd = ["x-terminal-emulator", "-e", "wifite"]
        self.run_cmd(cmd, "Running Wifite in new terminal")

    def run_cmd(self, cmd, desc):
        try:
            subprocess.Popen(cmd)
            self.log(f"{desc} started successfully")
        except Exception as e:
            self.log(f"Error running {desc}: {e}")
def check_sudo():
    if os.geteuid() != 0:
        root = tk.Tk()
        root.withdraw() 
        messagebox.showerror("Permission Denied", "❌ Please run this script with sudo/root privileges.")
        root.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFi_Emulator(root)
    root.mainloop()