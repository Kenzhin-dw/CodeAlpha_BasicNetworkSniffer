# Windows Installation

These steps target Windows 10/11 and PowerShell. Use the project only on a system or network you own or are authorized to monitor.

## 1. Install Python

Install a supported Python 3 release from [python.org](https://www.python.org/downloads/windows/). In the installer, select **Add python.exe to PATH**. This project was designed for Python 3.10 or newer.

Open a new PowerShell window and verify:

```powershell
python --version
python -m pip --version
```

If `python` opens the Microsoft Store or is not found, reopen the terminal after installation or use `py -3` in place of `python`.

## 2. Install Npcap

1. Download the current installer from the [official Npcap site](https://npcap.com/#download).
2. Right-click the installer and choose **Run as administrator**.
3. Keep **WinPcap API-compatible Mode** unchecked. Modern Scapy uses Npcap directly, and compatibility mode is not needed by this project.
4. The option to restrict the Npcap driver to administrators is acceptable; if enabled, the dashboard must be launched from an elevated terminal.
5. Complete the installation. Reboot if the installer requests it.

Do not install legacy WinPcap beside Npcap. Conflicting DLLs are a common cause of capture failures.

## 3. Obtain the project

Clone the repository if it is hosted:

```powershell
git clone <YOUR-REPOSITORY-URL>
cd CodeAlpha_BasicNetworkSniffer
```

For a downloaded ZIP, extract it and open PowerShell in the `CodeAlpha_BasicNetworkSniffer` folder.

## 4. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, allow it for this process only, then retry:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 5. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify imports:

```powershell
python -c "import scapy, pandas, streamlit; print('Dependencies OK')"
```

## 6. Launch with capture privileges

For the most predictable demonstration, close the terminal, right-click PowerShell, choose **Run as administrator**, return to the project, reactivate the environment, and launch:

```powershell
cd C:\path\to\CodeAlpha_BasicNetworkSniffer
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

Streamlit normally opens `http://localhost:8501`. If it does not, copy the Local URL printed by the terminal into a browser.

## 7. First capture

1. Keep **Auto (recommended)** selected in the sidebar. Use **All active interfaces** only if traffic spans multiple adapters or loopback.
2. Leave payload preview disabled for normal use.
3. Click **Start Capture**.
4. Click **Reset Display Filters**, then in a second terminal run `ping 8.8.8.8` and `nslookup example.com`.
5. Confirm that the table and charts update.
6. Click **Stop Capture**.
7. Click **Download filtered metadata as CSV** and save the file outside the repository or under the ignored `exports/` folder.

If nothing appears, use [troubleshooting.md](troubleshooting.md), especially the interface-selection and Npcap checks.
