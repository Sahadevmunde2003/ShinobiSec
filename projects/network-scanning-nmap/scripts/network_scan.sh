#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
OUTPUT_DIR="scans/automated"

if [[ -z "$TARGET" ]]; then
    echo "Usage: $0 <authorized-target>"
    echo "Example: $0 192.168.1.10"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "[+] Target: $TARGET"
echo "[+] Output: $OUTPUT_DIR"
echo "[+] Use only against an authorized lab target."

echo "[1/4] Host discovery..."
nmap -sn "$TARGET" -oN "$OUTPUT_DIR/host-discovery.txt"

echo "[2/4] TCP SYN scan..."
sudo nmap -sS "$TARGET" -oN "$OUTPUT_DIR/tcp-scan.txt"
echo "[3/4] Service/version detection..."
nmap -sV "$TARGET" -oN "$OUTPUT_DIR/service-detection.txt"
echo "[4/4] OS detection..."
sudo nmap -O "$TARGET" -oN "$OUTPUT_DIR/os-detection.txt"

echo
echo "[+] Scan complete."
echo "[+] Review files in $OUTPUT_DIR/"
