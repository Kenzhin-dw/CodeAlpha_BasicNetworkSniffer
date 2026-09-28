# Usage Guide

## Start and stop

Run `python -m streamlit run app.py`, keep **Auto (recommended)** selected, and click **Start Capture**. The status changes to `Running`. Generate ordinary traffic from the same computer, then click **Stop Capture** before ending the demo.

Streamlit reruns are safe: the capture manager is cached and refuses a second start while one sniffer is already running.

## Dashboard controls

- **Auto (recommended):** uses Scapy's default-route interface. This is normally the correct choice for DNS, HTTP, HTTPS, and ping traffic.
- **All active interfaces:** captures interfaces with usable IP addresses, including loopback. It can show duplicate broadcast or virtual-adapter traffic and uses more resources.
- **Advanced: show individual interfaces:** reveals the full adapter list only when a specific Wi-Fi, Ethernet, VPN, virtual, or loopback adapter is needed.
- **Optional sanitized payload preview:** off by default; affects only newly captured packets and stores at most 64 printable/sanitized bytes.
- **Start / Stop Capture:** manage the single background worker.
- **Clear Data:** remove in-memory metadata. It does not delete any downloaded file.
- **Protocol, Source IP, Destination IP:** filter dashboard statistics, table, details, and CSV export.
- **Reset Display Filters:** clears all three display filters. Use it before each safe test so an earlier ICMP filter does not hide DNS or TCP packets.
- **Maximum Displayed Packets:** limits table rendering, not the statistics or export dataset.
- **Auto Refresh:** updates the live dashboard fragment without spawning a new capture thread.

## Packet fields

The parser records timestamp, addresses, detailed protocol label, transport, ports, observed packet length, IP version, TCP flags, summary, payload presence, and payload length. Full payload bytes are not stored.

`HTTPS/TLS` means encrypted traffic commonly associated with TLS. The program does not decrypt it. Common ports are classification hints, not proof; layer evidence and visible HTTP start lines are checked where possible.

## CSV export

The download contains only:

`timestamp, src_ip, dst_ip, protocol, src_port, dst_port, length, payload_length`

Active filters apply to the export. Raw payload, preview, TCP flags, and summaries are deliberately excluded.

The dashboard states how many packets were captured and how many match the current filters. If total capture increases but matching packets remains zero, reset the filters rather than changing the capture interface.

## Ending a session

Stop capture first, close the browser tab, and press `Ctrl+C` in the Streamlit terminal. Do not commit real exports or packet captures.
