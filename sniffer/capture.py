"""Stable background packet capture built on Scapy AsyncSniffer."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from ipaddress import ip_address
from threading import RLock
from typing import Any, Optional

try:
    from scapy.all import AsyncSniffer, conf, get_if_list
except ImportError as exc:  # pragma: no cover - shown through the dashboard
    AsyncSniffer = None  # type: ignore[assignment]
    conf = None  # type: ignore[assignment]
    get_if_list = None  # type: ignore[assignment]
    SCAPY_IMPORT_ERROR: Optional[Exception] = exc
else:
    SCAPY_IMPORT_ERROR = None

from .parser import parse_packet

AUTO_INTERFACE = "__auto__"
ALL_INTERFACES = "__all__"


class CaptureState(str, Enum):
    STOPPED = "Stopped"
    RUNNING = "Running"
    ERROR = "Error"


@dataclass(frozen=True)
class CaptureStatus:
    state: CaptureState
    interface: Optional[str]
    error: Optional[str]
    packet_count: int


@dataclass(frozen=True)
class InterfaceOption:
    """One user-facing interface selection."""

    value: str
    label: str


class CaptureManager:
    """Own exactly one background sniffer and a bounded metadata buffer."""

    def __init__(self, capacity: int = 10_000) -> None:
        self._packets: deque[dict[str, Any]] = deque(maxlen=capacity)
        self._lock = RLock()
        self._sniffer: Any = None
        self._state = CaptureState.STOPPED
        self._interface: Optional[str] = None
        self._error: Optional[str] = None
        self._include_preview = False

    @staticmethod
    def interfaces() -> list[str]:
        if SCAPY_IMPORT_ERROR or get_if_list is None:
            return []
        try:
            return list(get_if_list())
        except (OSError, RuntimeError):
            return []

    @staticmethod
    def _interface_records() -> list[dict[str, str]]:
        """Return Scapy interfaces with readable Windows names."""
        if SCAPY_IMPORT_ERROR or conf is None:
            return []
        records: list[dict[str, str]] = []
        seen: set[str] = set()
        try:
            for interface in conf.ifaces.values():
                network_name = str(getattr(interface, "network_name", "") or "")
                if not network_name or network_name in seen:
                    continue
                is_valid = getattr(interface, "is_valid", None)
                if callable(is_valid) and not is_valid():
                    continue
                seen.add(network_name)
                records.append(
                    {
                        "network_name": network_name,
                        "name": str(getattr(interface, "name", "") or "Unknown interface"),
                        "description": str(getattr(interface, "description", "") or ""),
                        "ip": str(getattr(interface, "ip", "") or "No IP address"),
                    }
                )
        except (AttributeError, OSError, RuntimeError):
            return []
        return records

    @staticmethod
    def _has_usable_address(value: str) -> bool:
        try:
            address = ip_address(value)
        except ValueError:
            return False
        return address.is_loopback or not address.is_link_local

    @classmethod
    def _all_active_interfaces(cls) -> list[str]:
        """Select interfaces with a non-link-local IP, including loopback."""
        return [
            record["network_name"]
            for record in cls._interface_records()
            if cls._has_usable_address(record["ip"])
        ]

    @classmethod
    def interface_options(cls, include_individual: bool = False) -> list[InterfaceOption]:
        """Return simple defaults plus optional advanced interface choices."""
        if SCAPY_IMPORT_ERROR or conf is None:
            return []
        records = cls._interface_records()
        if not records:
            return []

        default_network_name = str(getattr(conf.iface, "network_name", "") or "")
        default_record = next(
            (record for record in records if record["network_name"] == default_network_name),
            records[0],
        )
        default_label = (
            f"Auto (recommended) — {default_record['name']} — {default_record['ip']}"
        )
        all_interfaces = cls._all_active_interfaces()
        options = [InterfaceOption(AUTO_INTERFACE, default_label)]
        if all_interfaces:
            options.append(
                InterfaceOption(
                    ALL_INTERFACES,
                    f"All active interfaces ({len(all_interfaces)} adapters; duplicates possible)",
                )
            )

        if include_individual:
            for record in sorted(records, key=lambda item: item["name"].lower()):
                description = record["description"]
                detail = f" — {description}" if description and description != record["name"] else ""
                options.append(
                    InterfaceOption(
                        record["network_name"],
                        f"{record['name']}{detail} — {record['ip']}",
                    )
                )
        return options

    @classmethod
    def _resolve_selection(cls, selection: str) -> tuple[str | list[str], str]:
        options = {option.value: option for option in cls.interface_options(True)}
        if selection not in options:
            raise ValueError("The selected interface is no longer available.")
        if selection == AUTO_INTERFACE:
            if conf is None:
                raise ValueError("Scapy interface configuration is unavailable.")
            target = str(getattr(conf.iface, "network_name", "") or "")
            if not target:
                raise ValueError("Scapy could not determine the default interface.")
            return target, options[selection].label
        if selection == ALL_INTERFACES:
            targets = cls._all_active_interfaces()
            if not targets:
                raise ValueError("No active interfaces with usable IP addresses were found.")
            return targets, options[selection].label
        return selection, options[selection].label

    def _on_packet(self, packet: Any) -> None:
        parsed = parse_packet(packet, self._include_preview)
        if parsed is not None:
            with self._lock:
                self._packets.append(parsed)

    def start(self, interface: str, include_payload_preview: bool = False) -> bool:
        """Start once. Returns False and records a user-facing error on failure."""
        with self._lock:
            if self._state == CaptureState.RUNNING:
                return True
            if SCAPY_IMPORT_ERROR or AsyncSniffer is None:
                self._set_error("Scapy is not installed. Run: pip install -r requirements.txt")
                return False
            if not interface:
                self._set_error("Select a network interface before starting capture.")
                return False
            self._include_preview = include_payload_preview
            self._error = None
            try:
                capture_target, display_label = self._resolve_selection(interface)
                self._interface = display_label
                self._sniffer = AsyncSniffer(
                    iface=capture_target,
                    prn=self._on_packet,
                    store=False,
                )
                self._sniffer.start()
                self._state = CaptureState.RUNNING
                return True
            except (OSError, PermissionError, RuntimeError, ValueError) as exc:
                self._sniffer = None
                self._set_error(self._friendly_error(exc))
                return False

    def stop(self) -> bool:
        with self._lock:
            if self._state != CaptureState.RUNNING:
                return True
            sniffer = self._sniffer
        try:
            if sniffer is not None:
                sniffer.stop(join=True)
        except (OSError, PermissionError, RuntimeError) as exc:
            with self._lock:
                self._set_error(self._friendly_error(exc))
            return False
        with self._lock:
            self._sniffer = None
            self._state = CaptureState.STOPPED
        return True

    def clear(self) -> None:
        with self._lock:
            self._packets.clear()

    def snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._packets)

    def status(self) -> CaptureStatus:
        with self._lock:
            if (
                self._state == CaptureState.RUNNING
                and self._sniffer is not None
                and not getattr(self._sniffer, "running", False)
            ):
                self._sniffer = None
                self._set_error(
                    "Capture stopped unexpectedly. Check Npcap, Administrator access, and the selected interface."
                )
            return CaptureStatus(self._state, self._interface, self._error, len(self._packets))

    def _set_error(self, message: str) -> None:
        self._state = CaptureState.ERROR
        self._error = message

    @staticmethod
    def _friendly_error(exc: Exception) -> str:
        message = str(exc).lower()
        if "winpcap" in message or "npcap" in message or "layer 2" in message:
            return "Npcap is unavailable. Install Npcap, then restart the terminal and application."
        if "permission" in message or "access" in message:
            return "Packet capture permission was denied. Restart the terminal as Administrator."
        return f"Capture could not start: {exc}"
