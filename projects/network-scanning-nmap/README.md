# Network Scanning & Host Discovery Using Nmap

A practical cybersecurity project demonstrating authorized network reconnaissance, host discovery, TCP port scanning, service/version enumeration, OS fingerprinting, basic packet analysis, and security finding documentation.

## Objectives
- Discover active hosts in an authorized lab network.
- Identify open TCP ports and exposed services.
- Enumerate service versions.
- Perform OS fingerprinting where permitted.
- Analyze scan traffic with Wireshark.
- Document findings and remediation recommendations.
- Automate repeatable Nmap scans with Bash.

## Lab Scope
Use only systems you own or have explicit authorization to test.

Example lab target: `192.168.1.0/24`

Replace this with your authorized lab subnet.

## Tools
- Nmap
- Kali Linux
- Bash
- Wireshark
- Zenmap (optional)

## Methodology
1. Define the authorized scope.
2. Identify the target subnet.
3. Perform host discovery.
4. Scan TCP ports.
5. Enumerate services and versions.
6. Perform OS detection where appropriate.
7. Analyze results.
8. Record evidence and findings.
9. Recommend remediation.
10. Retest after remediation.

## Commands

### Host discovery
```bash
nmap -sn 192.168.1.0/24 -oN scans/host-discovery.txt
```

### TCP SYN scan
```bash
sudo nmap -sS 192.168.1.10 -oN scans/tcp-scan.txt
```

### Service/version detection
```bash
nmap -sV 192.168.1.10 -oN scans/service-detection.txt
```

### OS detection
```bash
sudo nmap -O 192.168.1.10 -oN scans/os-detection.txt
```

### Combined assessment
```bash
sudo nmap -sS -sV -O 192.168.1.10 -oA scans/assessment
```

## Automation
```bash
chmod +x scripts/network_scan.sh
./scripts/network_scan.sh 192.168.1.10
```

The script saves results under `scans/automated/`.

## Findings
Use `findings/security-findings.md` to document evidence, affected host/port, risk, impact, recommendation, and retest status. Do not invent findings; populate them from real authorized lab results.

## Wireshark Analysis
Capture traffic while running a scan in your own lab and document source/destination IPs, TCP SYN packets, SYN/ACK responses, RST responses, and ICMP responses where applicable.

Suggested display filters:
```text
tcp.flags.syn == 1
tcp.flags.syn == 1 && tcp.flags.ack == 1
tcp.flags.reset == 1
icmp
```

## Learning Outcomes
- Network reconnaissance
- Host discovery
- TCP port scanning
- Service enumeration
- OS fingerprinting
- Bash automation
- Packet analysis
- Security assessment documentation

## Disclaimer
For educational and authorized security-testing purposes only. Never scan networks or systems without permission.
