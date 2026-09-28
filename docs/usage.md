# Usage Guide

## Start and stop

Run `python -m streamlit run app.py`, select an interface, and click **Start Capture**. The status changes to `Running`. Generate ordinary traffic from the same computer, then click **Stop Capture** before ending the demo.

Streamlit reruns are safe: the capture manager is cached and refuses a second start while one sniffer is already running.

## Dashboard controls

- **Network Interface:** choose the adapter carrying the traffic. Wi-Fi, Ethernet, VPN, and Npcap loopback are separate interfaces.
- **Optional sanitized payload preview:** off by default; affects only newly captured packets and stores at most 64 printable/sanitized bytes.
- **Start / Stop Capture:** manage the single background worker.
- **Clear Data:** remove in-memory metadata. It does not delete any downloaded file.
- **Protocol, Source IP, Destination IP:** filter dashboard statistics, table, details, and CSV export.
- **Maximum Displayed Packets:** limits table rendering, not the statistics or export dataset.
- **Auto Refresh:** updates the live dashboard fragment without spawning a new capture thread.

## Packet fields

The parser records timestamp, addresses, detailed protocol label, transport, ports, observed packet length, IP version, TCP flags, summary, payload presence, and payload length. Full payload bytes are not stored.

`HTTPS/TLS` means encrypted traffic commonly associated with TLS. The program does not decrypt it. Common ports are classification hints, not proof; layer evidence and visible HTTP start lines are checked where possible.

## CSV export

The download contains only:

`timestamp, src_ip, dst_ip, protocol, src_port, dst_port, length, payload_length`

Active filters apply to the export. Raw payload, preview, TCP flags, and summaries are deliberately excluded.

## Ending a session

Stop capture first, close the browser tab, and press `Ctrl+C` in the Streamlit terminal. Do not commit real exports or packet captures.

