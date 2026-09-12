# ShinobiSec Working Flowchart

```mermaid
flowchart TD
    A([Start ShinobiSec]) --> B[Open Command Center]
    B --> C{Select Jutsu}
    C --> D[Chidori - Nmap Host Scan]
    C --> E[Byakugan - Local Network Discovery]
    C --> F[Sharingan - Log Analysis]
    C --> G[Rasengan - Web Configuration Assessment]
    C --> H[Amaterasu - IOC & Threat Detection]
    C --> I[Shadow Clone - Parallel Defensive Analysis]
    D --> J[Run Authorized Assessment]
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J
    J --> K[Display Findings]
    K --> L{Generate Report?}
    L -->|Yes| M[Generate TXT Finding Report]
    M --> N[Download Report]
    L -->|No| O[Continue Assessment]
    N --> O
    O --> P{Chakra Remaining?}
    P -->|Yes| C
    P -->|0%| Q[Chakra Depleted]
    Q --> R[Emergency Shinobi Trial]
    R --> S[Select 5 Non-Repeating Questions]
    S --> T[Answer Naruto/Cybersecurity Quiz]
    T --> U{Correct?}
    U -->|Yes| V[+20% Chakra]
    U -->|No| W[+0% Chakra]
    V --> X{5 Questions Complete?}
    W --> X
    X -->|No| T
    X -->|Yes| Y[Save Used Questions in Browser]
    Y --> Z[Resume Mission]
    Z --> C
```

## Operational flow

1. Start the Flask application and open the ShinobiSec command center.
2. Select one of the six online Jutsu modules.
3. Provide module input and run the authorized assessment.
4. Review the findings displayed in the operation panel.
5. Generate and optionally download a text finding report.
6. Chakra is consumed by operations.
7. When chakra reaches 0%, the Emergency Shinobi Trial starts.
8. Five questions are selected while excluding previously used questions.
9. Correct answers restore 20% chakra; incorrect answers restore 0%.
10. Used-question IDs are stored in browser local storage until the question pool is exhausted.
11. After recovery, the user returns to the mission command center.

> Authorization: Run security assessment functions only against systems and networks you own or are explicitly authorized to test.
