# Network Scanning & Host Discovery Report

## 1. Executive Summary
This assessment evaluates an authorized laboratory network using Nmap to identify active hosts, exposed ports, services, and operating-system fingerprints.

## 2. Scope
- Target network: `<AUTHORIZED LAB RANGE>`
- Assessment date: `<DATE>`
- Tester: `<NAME>`
- Authorization: `<LAB / OWNER AUTHORIZATION>`

## 3. Tools
- Nmap
- Kali Linux
- Wireshark

## 4. Methodology
1. Host discovery
2. TCP port scanning
3. Service/version enumeration
4. OS detection
5. Wireshark traffic analysis
6. Findings and remediation

## 5. Results
| Host | Open Port | Protocol | Service | Version | Notes |
|---|---:|---|---|---|---|
| `<HOST>` | `<PORT>` | TCP | `<SERVICE>` | `<VERSION>` | `<NOTES>` |

## 6. Findings
Reference `../findings/security-findings.md`.

## 7. Recommendations
- Remove unnecessary services.
- Restrict management interfaces.
- Patch exposed services.
- Apply least-privilege firewall rules.
- Retest after remediation.

## 8. Limitations
Nmap results depend on network reachability, firewall behavior, permissions, scan configuration, and fingerprinting accuracy.

## 9. Conclusion
The assessment provides a baseline view of the authorized lab's network attack surface and identifies areas requiring further validation or hardening.
