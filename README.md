# ShinobiSec — Jutsu-Based Cybersecurity Assessment Framework

ShinobiSec is a Naruto-inspired cybersecurity command center that maps familiar Jutsu to practical defensive security tasks.

## Jutsu Arsenal

| Jutsu | Security function |
|---|---|
| ⚡ Chidori | Nmap reconnaissance and port analysis |
| 👁️ Sharingan | Security-log analysis and authentication detection |
| ◉ Byakugan | Authorized private-network host discovery |
| 🌀 Rasengan | Non-destructive HTTP/HTTPS configuration assessment |
| 🔥 Amaterasu | IOC and threat-pattern detection |
| 🥷 Shadow Clone | Parallel defensive analysis |

## Core features

- Single-page cybersecurity command center
- Nmap integration for authorized reconnaissance
- Local rule-based log and IOC analysis
- Web security-header checks
- Parallel defensive analysis
- TXT finding reports and downloads
- Chakra-based mission system
- Emergency Shinobi Trial when chakra reaches 0%
- Non-repeating Naruto/cybersecurity quiz with browser-persisted question history

## Working Flowchart

See [`docs/ShinobiSec_Workflow.md`](docs/ShinobiSec_Workflow.md) for the Mermaid source of the working flowchart. A PNG version is also included in the release archive when available.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

If Nmap is required on Kali/Debian:

```bash
sudo apt update
sudo apt install nmap
```

Then open `http://127.0.0.1:5000`.

## Authorization

Run network and web assessment functions only against systems and networks you own or are explicitly authorized to test. The framework is intentionally restricted and performs non-destructive checks where applicable.
