#!/bin/bash
CONFIG_FILE="path_config.conf"

# Erstellt die Konfigurationsdatei falls sie nicht existiert
if [ ! -f "$CONFIG_FILE" ]; then
    touch "$CONFIG_FILE"
fi

while true; do
    echo "Was m\u00f6chten Sie definieren?"
    echo "1) Output-Pfad"
    echo "2) Backup-Pfad"
    echo "3) Konfiguration anzeigen"
    echo "4) Beenden"
    read -rp "Auswahl: " choice
    case "$choice" in
        1)
            read -rp "Bitte Output-Pfad eingeben: " out
            # alte Definition entfernen
            grep -v '^OUTPUT_PATH=' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
            echo "OUTPUT_PATH=\"$out\"" >> "$CONFIG_FILE"
            ;;
        2)
            read -rp "Bitte Backup-Pfad eingeben: " back
            grep -v '^BACKUP_PATH=' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
            echo "BACKUP_PATH=\"$back\"" >> "$CONFIG_FILE"
            ;;
        3)
            if [ -s "$CONFIG_FILE" ]; then
                cat "$CONFIG_FILE"
            else
                echo "Keine Konfiguration vorhanden."
            fi
            ;;
        4)
            echo "Beende."
            break
            ;;
        *)
            echo "Ung\u00fcltige Auswahl."
            ;;
    esac
    echo
done
