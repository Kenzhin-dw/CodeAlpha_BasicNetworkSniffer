# Technical Video Recording Guide

Target length: approximately **5 minutes 30 seconds**. This is a project explanation and demonstration, not a coding tutorial.

## Before recording

- Install Npcap and run the project successfully from an Administrator PowerShell window.
- Close unrelated applications, browser tabs, notifications, and terminals.
- Keep optional payload preview disabled.
- Use ordinary test traffic only, such as `ping 8.8.8.8` and `nslookup example.com`.
- Hide or blur private IP addresses, adapter GUIDs, usernames, folder paths, and unrelated packet rows.
- Set the browser zoom so the dashboard, sidebar, and charts remain readable.
- Open these items in advance: `README.md`, `docs/architecture.md`, the running dashboard, `sniffer/capture.py`, `sniffer/parser.py`, `sniffer/statistics.py`, `utils/export.py`, and a terminal in the project folder.

## Recording flow

| Time | Section | What I say | What I show | File/page/terminal |
|---|---|---|---|---|
| 00:00–00:25 | Introduction | Introduce yourself, CodeAlpha, Task 1, and the project name. | README title and Task section. | `README.md` |
| 00:25–00:50 | Task objective | Explain capture, packet metadata, protocol learning, and the safe authorized scope. | README Objectives and requirement mapping. | `README.md` |
| 00:50–01:25 | Architecture | Explain interface → Npcap → AsyncSniffer → parser → protected buffer → statistics/dashboard → CSV. | Mermaid diagram. | `docs/architecture.md` |
| 01:25–01:50 | Technology | Explain why Python, Scapy, Npcap, Pandas, Streamlit, and Pytest are used. | Technology Stack section. | `README.md` |
| 01:50–03:00 | Live demonstration | Select the authorized interface, start capture, generate ICMP and DNS traffic, show metrics/table/chart/details, stop capture, and point out CSV export. | Dashboard and a second terminal. | Streamlit browser; PowerShell |
| 03:00–04:10 | Technical implementation | Explain lifecycle protection, parser behavior, protocol classification, statistics, and metadata-only export. | Short focused code sections; do not scroll through every file. | `capture.py`, `parser.py`, `protocols.py`, `statistics.py`, `export.py` |
| 04:10–04:35 | Testing/results | Run or show `python -m pytest -q`; state the verified result of 11 passing synthetic tests and the Windows/Npcap live diagnostic. | Test terminal and testing matrix. | PowerShell; `docs/testing.md` |
| 04:35–05:00 | Security and ethics | Explain authorization, disabled payload preview, no TLS decryption, metadata-only CSV, and ignored capture files. | Security/Ethics and `.gitignore`. | `README.md`; `.gitignore` |
| 05:00–05:20 | Limitations | Mention selected-interface visibility, best-effort application labels, TLS encryption, and the bounded educational design. | Limitations section. | `README.md` |
| 05:20–05:40 | Conclusion | Summarize what was built and what you learned. | Final dashboard or README title. | Dashboard or `README.md` |

## Live demonstration sequence

1. Show the dashboard in `Stopped` state.
2. Keep **Auto (recommended)** selected. The individual GUID list is hidden unless Advanced is enabled.
3. Confirm that payload preview is off.
4. Click **Reset Display Filters**, then click **Start Capture**.
5. In the terminal, run:

   ```powershell
   ping 8.8.8.8
   nslookup example.com
   ```

6. Return to the dashboard and show the metric cards, live table, protocol chart, timeline, and one safe packet detail.
7. If background traffic is noisy, apply the ICMP or DNS protocol filter.
8. Click **Stop Capture**.
9. Point to the CSV download button, but do not open a real capture export on screen. Use `sample/sample_packets.csv` if a CSV example is needed.

If capture does not work, do not pretend that it does. Pause the recording, use `docs/troubleshooting.md`, fix Npcap/interface/permission problems, and restart the recording only after a clean manual test.

## Presentation tips

- Read ideas, not every code line.
- Keep source-code zoom large enough to show the relevant function only.
- Pause briefly when moving between the browser, terminal, and editor.
- Do not show the GitHub authentication flow, email address, notifications, or saved credentials.
- Record one short clean demonstration rather than a long unedited debugging session.
