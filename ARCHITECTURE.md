# ShinobiSec Architecture

## High-level design

```text
Browser UI
   |
   v
Flask Application (app.py)
   |
   +--> Chidori      -> Nmap reconnaissance
   +--> Byakugan     -> private-network host discovery
   +--> Sharingan    -> security-log analysis
   +--> Rasengan     -> HTTP/HTTPS configuration checks
   +--> Amaterasu    -> IOC/threat-pattern detection
   +--> Shadow Clone -> parallel defensive analysis
   |
   v
Findings -> Report Generator -> TXT report
   |
   v
Chakra System -> Emergency Shinobi Trial -> localStorage question history
```

## Security design principles

- Validate and constrain user-controlled assessment targets.
- Use non-destructive checks where possible.
- Execute Nmap without shell interpretation.
- Keep analysis local and deterministic where practical.
- Separate assessment results from report generation.
- Require authorization for all network and web assessment activity.

## Main components

| Component | Responsibility |
|---|---|
| `app.py` | Flask routes, validation, security-analysis logic and Nmap integration |
| `templates/index.html` | Single-page command-center UI |
| `static/script.js` | Jutsu controls, API calls, reports, chakra and quiz logic |
| `static/style.css` | Command-center presentation layer |
| `docs/ShinobiSec_Workflow.md` | Detailed operational flowchart |
