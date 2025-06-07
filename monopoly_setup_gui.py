#!/usr/bin/env python3
"""GUI frontend for the MonopolyGo setup script."""

import os
import glob
import subprocess
import urllib.request
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox

BASE_URL = "https://hosting216477.ae984.netcup.net"
DOWNLOADS = "/storage/emulated/0/MonopolyGo/Downloads"
ZIEL = "/storage/emulated/0/MonopolyGo"
APK_DIR = os.path.join(ZIEL, "Anwendungen")

ZIP_LIST = [
    "Accounts.zip",
    "Anwendungen.zip",
    "Medien.zip",
    "Script.zip",
    "Tasker.zip",
    "Website.zip",
]

APK_TARGETS = [
    "Acc_Manager.9.apk",
    "MiXplorer_24112322_6.68.4.apk",
]

class SetupApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MonopolyGo Setup")
        self.geometry("600x400")

        self.start_btn = ttk.Button(self, text="Download + Install", command=self.run)
        self.start_btn.pack(pady=10)

        self.log_text = tk.Text(self, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log(self, msg: str) -> None:
        """Append a line to the log textbox."""
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.update()

    def run(self) -> None:
        self.start_btn["state"] = tk.DISABLED
        os.makedirs(DOWNLOADS, exist_ok=True)
        os.makedirs(ZIEL, exist_ok=True)
        self.log("\U0001F680 Starte Download und Entpacken ...")

        for zip_name in ZIP_LIST:
            self.log(f"\u2B07\uFE0F  Lade: {zip_name} ...")
            zip_url = f"{BASE_URL}/{zip_name}"
            zip_path = os.path.join(DOWNLOADS, zip_name)
            try:
                urllib.request.urlretrieve(zip_url, zip_path)
            except Exception as exc:
                self.log(f"\u274C Download fehlgeschlagen: {zip_name} ({exc})")
                continue

            ordner_name = zip_name[:-4]
            ziel_ordner = os.path.join(ZIEL, ordner_name)
            if os.path.isdir(ziel_ordner):
                self.log(f"\u26A0\uFE0F  Ordner existiert schon: {ordner_name} – übersprungen")
            else:
                self.log(f"\U0001F4E6 Entpacke {zip_name} nach {ZIEL} ...")
                try:
                    with zipfile.ZipFile(zip_path) as zf:
                        zf.extractall(ZIEL)
                    self.log(f"\u2705 Entpackt: {zip_name}")
                except Exception as exc:
                    self.log(f"\u274C Entpackfehler: {zip_name} ({exc})")

        self.log("")
        self.log("\U0001F4F2 Installiere relevante APKs (sofern vorhanden & möglich)...")

        for apk in APK_TARGETS:
            apk_path = os.path.join(APK_DIR, apk)
            if os.path.isfile(apk_path):
                self.log(f"\U0001F4E6 Installiere {apk} ...")
                subprocess.run(["pm", "install", "-r", apk_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                self.log(f"\u26A0\uFE0F  {apk} nicht gefunden.")

        for apk_path in glob.glob(os.path.join(APK_DIR, "Elite_vE*.apk")):
            self.log(f"\U0001F4E6 Installiere Elite: {os.path.basename(apk_path)}")
            subprocess.run(["pm", "install", "-r", apk_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        self.log("")
        self.log("\U0001F3C1 Setup abgeschlossen.")
        messagebox.showinfo("Fertig", "Setup abgeschlossen.")
        self.start_btn["state"] = tk.NORMAL


def main() -> None:
    app = SetupApp()
    app.mainloop()


if __name__ == "__main__":
    main()
