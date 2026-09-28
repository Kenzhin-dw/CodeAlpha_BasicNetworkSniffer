# English Technical Video Transcript

Stage directions in square brackets are actions only. Do not read them aloud.

## 1. Introduction — 00:00 to 00:25

[SHOW: `README.md`, with the title and Task section visible.]

Hello everyone. My name is Ihsan.

In this video, I will present my project for the CodeAlpha Cyber Security Internship, Task 1: Basic Network Sniffer.

The project is called Network Packet Sniffer and Traffic Analyzer. It captures authorized Windows network traffic and presents packet metadata in a web dashboard.

## 2. Project objective — 00:25 to 00:50

[SHOW: README Objectives and Internship Requirement Mapping.]

The task requires a Python program that captures packets and displays the source IP, destination IP, protocol, and payload information.

I implemented these requirements with a privacy-focused design. The application shows packet metadata, payload presence, and payload length. It does not store or export full raw payload.

It is intended only for systems and networks that I own or have permission to inspect.

## 3. Architecture — 00:50 to 01:25

[SHOW: the diagram in `docs/architecture.md`.]

The workflow starts at a selected Windows network interface.

Npcap provides packet access. Scapy runs one background AsyncSniffer and sends each packet to the parser.

The parser converts IPv4 and IPv6 packets into dictionaries stored in a bounded, lock-protected buffer.

Streamlit reads a snapshot of the buffer for the table and statistics. A separate export function creates a CSV with approved metadata columns only.

## 4. Technology stack — 01:25 to 01:50

[SHOW: README Technology Stack.]

Python is the main language. Scapy handles packet capture and protocol layers, while Npcap provides the Windows capture driver.

Pandas supports tables and the packet timeline. Streamlit provides the dashboard. Pytest runs automated tests with synthetic packets.

The code keeps capture, parsing, statistics, export, and the interface separate.

## 5. How the system works and live demonstration — 01:50 to 03:00

[SHOW: the application in `Stopped` state.]

This is the dashboard. The sidebar contains interface selection, capture controls, filters, and refresh settings.

I select this computer's active interface and keep payload preview disabled.

[ACTION: Select the authorized interface and click **Start Capture**.]

The status is now running. Capture works in the background, so the interface remains responsive.

[SHOW: PowerShell. Run `ping 8.8.8.8`, then `nslookup example.com`.]

I am generating ordinary ICMP and DNS traffic from the same computer.

[SHOW: return to the dashboard.]

The cards show packet and transport counts. The table shows time, endpoints, protocol, ports, and length.

The charts show protocol distribution, frequent endpoints, and packet activity over time.

[ACTION: Apply the ICMP or DNS filter if useful, then select one safe packet.]

The detail view shows IP version, TCP flags, a summary, and payload length. It does not decrypt HTTPS.

[ACTION: Click **Stop Capture** and point to the CSV button.]

After stopping, filtered metadata can be downloaded as CSV. Payload preview is excluded.

## 6. Important technical implementation — 03:00 to 04:10

[SHOW: `sniffer/capture.py`, focused on `CaptureManager`.]

CaptureManager owns one AsyncSniffer and a deque limited to ten thousand records. An RLock protects shared data. `st.cache_resource` keeps one manager across Streamlit reruns, and the start method rejects a duplicate capture thread.

[SHOW: `sniffer/parser.py`, focused on `parse_packet`.]

The parser accepts IPv4 and IPv6 packets. It extracts addresses, ports, length, IP version, TCP flags, a summary, and payload metadata. Non-IP packets are ignored. Optional preview text is sanitized and limited to sixty-four bytes.

[SHOW: `sniffer/protocols.py`.]

Protocol identification uses several signals. DNS and ICMP use Scapy layers. Visible HTTP start lines identify HTTP-like data. Common ports add service hints. The labels remain best-effort because a port alone cannot prove the application protocol.

[SHOW: `sniffer/statistics.py` and `utils/export.py`.]

The statistics module calculates totals, bytes, average size, top endpoints, ports, and time buckets. The CSV exporter allowlists eight fields, preventing summaries or previews from entering the file.

## 7. Testing and results — 04:10 to 04:35

[SHOW: terminal. Run `python -m pytest -q`.]

The tests create synthetic Scapy packets and do not need capture privileges.

The final audit passed ten tests covering packet parsing, sanitized previews, statistics, timeline grouping, empty input, and safe CSV export.

Streamlit AppTest also loaded the dashboard without an application exception. Live capture still depends on Npcap, interface choice, and Windows permissions.

## 8. Security and ethics — 04:35 to 05:00

[SHOW: README Security / Ethics and `.gitignore`.]

This project is only for educational and authorized monitoring.

It does not inject or spoof packets, harvest credentials, hijack sessions, or decrypt TLS. Preview is disabled by default, and `.gitignore` excludes captures, exports, secrets, logs, and keys.

The sample CSV uses reserved documentation addresses, not real captured data.

## 9. Limitations — 05:00 to 05:20

[SHOW: README Limitations.]

The program sees only the selected interface. Application labels are best-effort, and TLS content remains encrypted. The bounded buffer makes this an educational dashboard, not a lossless forensic capture tool.

## 10. Conclusion — 05:20 to 05:40

[SHOW: the final dashboard or README title.]

Overall, this project demonstrates authorized packet capture, protocol-aware parsing, thread-safe processing, statistics, and privacy-conscious export.

I learned how packet layers become structured data and how to present them safely.

Thank you for watching.

