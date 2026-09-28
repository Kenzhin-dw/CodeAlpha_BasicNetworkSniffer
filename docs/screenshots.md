# Internship Screenshot Checklist

Use synthetic or ordinary demonstration traffic. Crop or blur public IP addresses, private IP addresses when required by your organization, interface GUIDs, hostnames, usernames, browser tabs, filesystem usernames, and any payload preview. Never show credentials, cookies, tokens, email contents, or private browsing activity.

| File name | What should be visible | Why it matters | Hide before submission |
|---|---|---|---|
| `01-python-version.png` | PowerShell running `python --version` | Proves Python is installed | Username/path if required |
| `02-npcap-installed.png` | Npcap entry in Windows Installed Apps or installer completion | Proves capture driver setup | Unrelated installed applications |
| `03-application-startup.png` | Streamlit dashboard, `Stopped` state, empty-state message | Shows clean startup and error handling | Browser history/tabs |
| `04-interface-selection.png` | Interface dropdown with the chosen adapter | Shows configurable capture source | Adapter GUIDs and organization names |
| `05-live-packet-capture.png` | `Running` state and populated live table | Demonstrates core requirement | Sensitive addresses/hostnames |
| `06-icmp-capture.png` | `ping` command plus filtered ICMP dashboard rows | Demonstrates ICMP recognition | Public/private addressing as needed |
| `07-dns-capture.png` | `nslookup example.com` plus DNS rows/count | Demonstrates DNS recognition | Resolver address if sensitive |
| `08-tcp-udp-capture.png` | Table containing TCP and UDP examples with ports | Demonstrates transport parsing | Unrelated traffic |
| `09-protocol-chart.png` | Protocol Distribution chart | Demonstrates statistics | Sensitive labels if any |
| `10-top-source-destination.png` | Both top IP charts | Demonstrates traffic analysis | Real infrastructure IPs; use blur or test data |
| `11-packet-details.png` | Safe metadata fields and payload length | Demonstrates packet structure analysis | Payload preview, precise private identifiers |
| `12-csv-export.png` | Download action and opened CSV header/one sanitized row | Demonstrates required export | Real capture rows; use synthetic/sanitized data |
| `13-final-dashboard.png` | Full dashboard with metrics, table, charts, timeline | Portfolio overview | All identifying or private data |

Use consistent browser zoom and window size. Ensure the authorization notice and project title appear in the final dashboard screenshot.

