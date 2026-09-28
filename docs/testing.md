# Safe Testing

Run tests only from a computer and network you are authorized to inspect.

## Automated tests

With the virtual environment active:

```powershell
python -m pytest -q
```

The tests construct synthetic Scapy packets. They do not capture live traffic and verify parser behavior, statistics, timeline grouping, privacy-safe previews, and CSV allowlisting.

## Manual live-capture procedure

Start the dashboard as Administrator, choose the active adapter, click **Start Capture**, and use a second terminal for these checks.

### ICMP test

```powershell
ping 8.8.8.8
```

Expected: ICMP packets between the local address and `8.8.8.8`. Some networks block ICMP; a timeout does not necessarily mean the sniffer is faulty.

### DNS test

```powershell
nslookup example.com
```

Expected: DNS traffic, normally UDP port 53, between the computer and its configured resolver. A cached answer or encrypted DNS configuration can change what is visible.

### HTTP test

Use plain HTTP only as a controlled protocol-demonstration endpoint:

```powershell
curl.exe http://example.com/
```

Expected: TCP port 80 and, when a visible HTTP start line is in a captured segment, an `HTTP` label. Redirects may then create HTTPS traffic. Do not submit credentials or private data over HTTP.

### HTTPS test

```powershell
curl.exe https://example.com/
```

Expected: TCP/`HTTPS/TLS` traffic, commonly on port 443. The dashboard must not show decrypted page content because TLS protects application data.

### Local HTTP test

Terminal 1:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Terminal 2:

```powershell
curl.exe http://127.0.0.1:8000/
```

Select the **Npcap Loopback Adapter** to observe this traffic. Selecting Wi-Fi or Ethernet normally will not show loopback packets. Stop the server with `Ctrl+C`.

## Testing matrix

Fill the Actual and Status columns during the target-machine demonstration.

| Test ID | Feature | Expected | Actual | Status |
|---|---|---|---|---|
| UNIT-001 | Automated suite | All synthetic tests pass | 10 passed | PASS |
| NET-001 | ICMP capture | ICMP packet displayed | To verify on target Windows machine | Pending |
| NET-002 | DNS capture | DNS traffic displayed | To verify on target Windows machine | Pending |
| NET-003 | TCP capture | TCP metadata and ports displayed | To verify on target Windows machine | Pending |
| NET-004 | UDP capture | UDP metadata and ports displayed | To verify on target Windows machine | Pending |
| NET-005 | HTTPS privacy | TLS metadata; no decrypted content | To verify on target Windows machine | Pending |
| NET-006 | Stop/restart | One capture worker; UI remains responsive | To verify on target Windows machine | Pending |
| NET-007 | Filters | Table, metrics, charts, and export reflect filters | To verify on target Windows machine | Pending |
| NET-008 | CSV export | Eight approved columns; no preview/raw payload | Covered automatically and verify download | Pending |
