# Video Cheat Sheet

Keep payload preview off. Hide IPs, GUIDs, usernames, and unrelated traffic.

## 00:00 — Introduction

- Ihsan
- CodeAlpha Cyber Security Internship
- Task 1: Basic Network Sniffer
- Network Packet Sniffer & Traffic Analyzer
- Show: README title

## 00:25 — Objective

- Capture authorized local traffic
- Source IP, destination IP, protocol, payload metadata
- No full raw payload by default
- Show: Objectives and requirement mapping

## 00:50 — Architecture

- Interface → Npcap → Scapy AsyncSniffer
- Parser → bounded `deque` + `RLock`
- Snapshot → statistics + Streamlit
- Eight-column CSV allowlist
- Show: `docs/architecture.md`

## 01:25 — Technology

- Python: application logic
- Scapy + Npcap: Windows capture and layers
- Pandas: tables/timeline
- Streamlit: dashboard
- Pytest: synthetic tests

## 01:50 — Live demo

- Show dashboard stopped
- Keep Auto (recommended); preview OFF; reset filters
- Start capture
- Run `ping 8.8.8.8`
- Run `nslookup example.com`
- Show metrics, table, chart, timeline, safe details
- Filter ICMP/DNS if needed
- Stop capture; point to CSV button

## 03:00 — Implementation

- `capture.py`: one sniffer, cached manager, lock, 10,000-record bound
- `parser.py`: IPv4/IPv6, ports, flags, length, safe payload metadata
- `protocols.py`: layers + HTTP start line + port hints
- `statistics.py`: counts, bytes, top endpoints/ports, timeline
- `export.py`: approved columns only

## 04:10 — Testing

- Run `python -m pytest -q`
- Factual result: 11 passed
- Streamlit AppTest: no application exception
- Live diagnostic verified DNS, HTTP, HTTPS/TLS, TCP, and UDP metadata

## 04:35 — Security and ethics

- Authorized use only
- No injection, spoofing, harvesting, or decryption
- Preview disabled by default
- Synthetic sample IPs
- `.gitignore` blocks captures, exports, logs, secrets, keys

## 05:00 — Limitations

- Selected-interface visibility only
- Best-effort application labels
- TLS stays encrypted
- Educational, bounded in-memory design

## 05:20 — Conclusion

- Packet capture + parsing + statistics + dashboard + safe export
- Learned network-layer data flow and privacy controls
- Thank viewers
