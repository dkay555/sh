# sh

Collection of small shell scripts.

## extract_url_from_clipboard.sh

This script extracts the first URL from the clipboard and saves it to a file.
After extracting the URL, it asks for a quantity (`Anzahl`) and a name.
The script appends a CSV line in the format `Name,Anzahl,Link` to the
specified output file (default `clipboard_url.txt`).

## monopoly_setup_gui.py

Tkinter-basierte GUI, die den Download, das Entpacken und die Installation
von APK-Dateien wie im ursprünglichen Termux-Skript durchführt. Innerhalb
von Termux kann mit einem Klick auf „Download + Install“ der komplette
Prozess gestartet werden.
