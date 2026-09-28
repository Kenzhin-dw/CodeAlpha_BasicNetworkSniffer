# Safe Testing

Run tests only from a computer and network you are authorized to inspect.

## Automated tests

With the virtual environment active:

```powershell
python -m pytest -q
```

The tests construct synthetic Scapy packets. They do not capture live traffic and verify parser behavior, statistics, timeline grouping, privacy-safe previews, and CSV allowlisting.

## Manual live-capture procedure

Start the dashboard as Administrator, keep **Auto (recommended)** selected, click **Start Capture**, and use a second terminal for these checks. Before every test, click **Reset Display Filters**. If Auto does not cover the required adapter or localhost traffic, stop capture and retry with **All active interfaces**.

### ICMP test

```powershell
ping 8.8.8.8
```

Expected: ICMP packets between the local address and `8.8.8.8`. Some networks block ICMP; a timeout does not necessarily mean the sniffer is faulty.

### DNS test

```powershell
ipconfig /flushdns
nslookup example.com
```

Expected: `DNS` rows, normally UDP port 53, between the computer and its configured resolver. The Protocol Distribution chart has a separate DNS category. A browser may use encrypted DNS, but `nslookup` normally generates ordinary DNS traffic.

### HTTP test

Use plain HTTP only as a controlled protocol-demonstration endpoint:

```powershell
curl.exe --http1.1 -I http://example.com/
```

Expected: TCP port 80 and an `HTTP` label when the request or response start line is visible. The protocol chart groups HTTP under TCP. Redirects may also create HTTPS traffic. Do not submit credentials or private data over HTTP.

### HTTPS test

```powershell
curl.exe --http1.1 -I https://example.com/
```

Expected: TCP/`HTTPS/TLS` rows, commonly on port 443. The protocol chart groups HTTPS/TLS under TCP. The dashboard must not show decrypted page content because TLS protects application data.

### Local HTTP test

Terminal 1:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Terminal 2:

```powershell
curl.exe http://127.0.0.1:8000/
```

Select **All active interfaces**, or enable Advanced and select the loopback adapter, to observe this traffic. Wi-Fi alone normally will not show loopback packets. Stop the server with `Ctrl+C`.

## If only ICMP is visible

1. Click **Reset Display Filters**. An ICMP filter from the previous test will hide DNS, HTTP, and HTTPS rows even while they are being captured.
2. Confirm **Total Captured** continues increasing. If it increases but the table is empty, a display filter is still active.
3. Stop capture, choose **Auto (recommended)**, clear data, and start again.
4. Run the exact `nslookup` and `curl.exe` commands above.
5. Look in the live table: HTTP and HTTPS are grouped as TCP in the distribution chart, while their detailed labels appear in the table.
6. If Auto still misses traffic, stop and retry **All active interfaces**. Duplicate packets are possible in this mode.

## Testing matrix

Fill the Actual and Status columns during the target-machine demonstration.

| Test ID | Feature | Expected | Actual | Status |
|---|---|---|---|---|
| UNIT-001 | Automated suite | All synthetic tests pass | 11 passed | PASS |
| NET-001 | ICMP capture | ICMP packet displayed | Reported working on target machine | PASS |
| NET-002 | DNS capture | DNS traffic displayed | Live diagnostic captured DNS-layer traffic in Auto and All-active modes | PASS |
| NET-003 | TCP capture | TCP metadata and ports displayed | Live diagnostic captured TCP plus HTTP and HTTPS/TLS labels | PASS |
| NET-004 | UDP capture | UDP metadata and ports displayed | Live diagnostic captured UDP and port 53 traffic | PASS |
| NET-005 | HTTPS privacy | TLS metadata; no decrypted content | Port 443 metadata captured; application content remains encrypted | PASS |
| NET-006 | Stop/restart | One capture worker; UI remains responsive | Auto and All-active managers started and stopped successfully | PASS |
| NET-007 | Filters | Table, metrics, charts, and export reflect filters | To verify on target Windows machine | Pending |
| NET-008 | CSV export | Eight approved columns; no preview/raw payload | Covered automatically and verify download | Pending |
