"""Stable background packet capture built on Scapy AsyncSniffer."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Any, Optional

try:
    from scapy.all import AsyncSniffer, get_if_list
except ImportError as exc:  # pragma: no cover - shown through the dashboard
    AsyncSniffer = None  # type: ignore[assignment]
    get_if_list = None  # type: ignore[assignment]
    SCAPY_IMPORT_ERROR: Optional[Exception] = exc
else:
    SCAPY_IMPORT_ERROR = None

from .parser import parse_packet


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
            if interface not in self.interfaces():
                self._set_error("The selected interface is no longer available. Refresh and select another interface.")
                return False
            self._include_preview = include_payload_preview
            self._interface = interface
            self._error = None
            try:
                self._sniffer = AsyncSniffer(iface=interface, prn=self._on_packet, store=False)
                self._sniffer.start()
                self._state = CaptureState.RUNNING
                return True
            except (OSError, PermissionError, RuntimeError) as exc:
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
