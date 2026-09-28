# Windows Troubleshooting

## No packets captured

**Cause:** wrong interface, no new traffic, capture permission, or a disconnected adapter.  
**How to check:** run `ping 8.8.8.8`, inspect the status, and compare the selected adapter with the active adapter in `ipconfig`.  
**Fix:** select active Wi-Fi/Ethernet, run PowerShell as Administrator, stop/start capture, and generate fresh traffic.

## Npcap not found

**Cause:** Npcap is missing, installation did not complete, or legacy WinPcap conflicts with it.  
**How to check:** open Windows Installed Apps and find Npcap; run `Get-Service npcap` in elevated PowerShell.  
**Fix:** uninstall legacy WinPcap, install current Npcap from the official site, keep WinPcap compatibility mode off, and reboot if requested.

## Permission denied

**Cause:** Npcap was installed with administrator-only access or the device ACL blocks the process.  
**How to check:** compare behavior in a normal versus elevated PowerShell window.  
**Fix:** launch PowerShell with **Run as administrator**, activate the environment, and restart Streamlit.

## No interfaces available

**Cause:** Scapy cannot reach Npcap, the driver is stopped, or requirements are absent.  
**How to check:** run `python -c "from scapy.all import get_if_list; print(get_if_list())"`.  
**Fix:** reinstall requirements and Npcap, restart Windows if needed, then relaunch the app.

## Wrong interface selected

**Cause:** traffic uses Wi-Fi while Ethernet/VPN/virtual/loopback was selected.  
**How to check:** use `ipconfig` and note which adapter owns the current local address/default gateway.  
**Fix:** stop capture, select that adapter, and start again. Use Npcap Loopback only for `127.0.0.1`/`::1` tests.

## Streamlit keeps rerunning

**Cause:** reruns are normal after widgets and during optional fragment auto-refresh.  
**How to check:** the status should stay `Running` and the capture count should grow without multiple terminal processes.  
**Fix:** turn off Auto Refresh for a static view. Do not launch a second Streamlit process.

## Capture thread duplicated

**Cause:** usually two Streamlit server processes or browser sessions using separate servers, not a normal app rerun.  
**How to check:** inspect running terminals and `Get-Process python`.  
**Fix:** stop extra servers with `Ctrl+C`. The manager itself rejects `start()` while already running.

## Dashboard freezes or becomes slow

**Cause:** very high packet rate, a large display limit, or rapid refresh.  
**How to check:** stop capture; if the UI recovers, reduce rendering work.  
**Fix:** display 250 or fewer packets, use a 3–5 second refresh, apply a filter, and keep payload preview off.

## Scapy cannot access an interface

**Cause:** adapter was disconnected/removed, permissions changed, or Npcap/WinPcap DLL conflict.  
**How to check:** refresh the app and rerun the Scapy interface-list command above.  
**Fix:** reconnect the adapter, remove legacy WinPcap, repair Npcap, and restart elevated.

## Localhost traffic is not captured

**Cause:** loopback traffic does not traverse Wi-Fi or Ethernet.  
**How to check:** confirm the request targets `127.0.0.1` and look for the Npcap Loopback Adapter.  
**Fix:** stop capture, select the loopback interface, restart capture, then repeat the request.

## Odd checksums or unexpectedly large packets

**Cause:** NIC checksum/segmentation offload can alter how locally captured packets appear.  
**How to check:** compare with traffic captured at another point only if authorized.  
**Fix:** treat this as an observation artifact for this educational dashboard. Disabling adapter offload is usually unnecessary.

## No visible HTTP label

**Cause:** the site redirected to HTTPS, the HTTP start line was not in the captured segment, or a nonstandard protocol uses the port.  
**How to check:** use the documented controlled `curl.exe http://example.com/` test and inspect TCP rows.  
**Fix:** accept TCP classification as valid metadata. Port and payload-based application identification is best-effort.

