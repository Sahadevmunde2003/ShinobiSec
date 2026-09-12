# ⚡ ShinobiSec

### Jutsu-Based Cybersecurity Assessment Framework

> A Naruto-inspired cybersecurity command center mapping Jutsu to practical security assessment and defensive analysis workflows.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white) ![Nmap](https://img.shields.io/badge/Nmap-Network%20Recon-2F6BFF) ![Security](https://img.shields.io/badge/Focus-Cybersecurity-critical) ![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Overview

ShinobiSec is a single-page cybersecurity command center designed to demonstrate practical security concepts through a themed Jutsu system. It combines network reconnaissance, security-log analysis, web configuration assessment, IOC detection, and parallel defensive analysis in one Flask-based interface.

## 🥷 Jutsu Arsenal

| Jutsu | Capability | Security Focus |
|---|---|---|
| ⚡ **Chidori** | Nmap host/port scan | Network reconnaissance |
| 👁️ **Sharingan** | Log analysis | Authentication & privilege events |
| ◉ **Byakugan** | Private-network discovery | Host visibility |
| 🌀 **Rasengan** | HTTP/HTTPS assessment | Security headers & cookies |
| 🔥 **Amaterasu** | IOC detection | Threat indicators & suspicious patterns |
| 🥷 **Shadow Clone** | Parallel analysis | Defensive workflow automation |

## ✨ Features

- Single-page cybersecurity command center
- Authorized Nmap reconnaissance
- Rule-based security-log analysis
- Private-network host discovery
- HTTP/HTTPS security configuration checks
- IOC and threat-pattern detection
- Parallel defensive analysis
- Finding generation and TXT report downloads
- Chakra-based mission system
- Emergency Shinobi Trial at 0% chakra
- 40-question Naruto + cybersecurity quiz bank
- Non-repeating quiz selection using browser `localStorage`
- Demo test data for quick evaluation

## 🏗️ Architecture

```text
Browser UI → Flask Application
                  ├─ Chidori → Nmap reconnaissance
                  ├─ Byakugan → Private-network discovery
                  ├─ Sharingan → Log analysis
                  ├─ Rasengan → Web configuration checks
                  ├─ Amaterasu → IOC/threat detection
                  └─ Shadow Clone → Parallel defensive analysis
                              ↓
                         Findings → TXT Reports
                              ↓
                    Chakra → Emergency Trial → Quiz Recovery
```

See [`ARCHITECTURE.md`](ARCHITECTURE.md) and [`docs/ShinobiSec_Workflow.md`](docs/ShinobiSec_Workflow.md) for detailed diagrams.

## 🛠️ Tech Stack

**Backend:** Python, Flask  
**Frontend:** HTML, CSS, JavaScript  
**Security Tool:** Nmap  
**State:** Browser localStorage and in-memory analysis  
**Platforms:** Kali Linux, Debian, Ubuntu, Windows

## 🚀 Installation

```bash
git clone https://github.com/Sahadevmunde2003/ShinobiSec.git
cd ShinobiSec
pip install -r requirements.txt
python app.py
```

Kali/Debian Nmap installation:

```bash
sudo apt update
sudo apt install nmap
```

Open `http://127.0.0.1:5000`.

## 🧪 Quick Demo

Use **LOAD DEMO DATA** in the command center for safe example inputs. See [`DEMO_TEST_DATA.txt`](DEMO_TEST_DATA.txt) for the complete test set.

## 🔐 Security & Authorization

ShinobiSec is intended for **authorized security testing and defensive analysis only**. Test only systems and networks you own or have explicit permission to assess. Network discovery is constrained, web checks are configuration-oriented and non-destructive, and Nmap execution avoids shell interpretation.

See [`SECURITY.md`](SECURITY.md).

## 🗺️ Roadmap

- [x] Six Jutsu modules
- [x] Finding reports
- [x] Chakra recovery system
- [x] Non-repeating quiz system
- [ ] SQLite-backed assessment history
- [ ] Structured JSON/PDF reporting
- [ ] Authentication and role-based access
- [ ] Automated test suite and CI
- [ ] Expanded defensive analytics

## 📁 Project Structure

```text
ShinobiSec/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── DEMO_TEST_DATA.txt
├── ARCHITECTURE.md
├── docs/
│   └── ShinobiSec_Workflow.md
├── templates/index.html
└── static/
    ├── script.js
    └── style.css
```

## 👤 Author

**Sahadev Munde**  
Cybersecurity | SOC | Network Security | Ethical Hacking

GitHub: [@Sahadevmunde2003](https://github.com/Sahadevmunde2003)

## 📄 License

MIT License — see [`LICENSE`](LICENSE).
