"""Protocol and common service identification helpers."""

from __future__ import annotations

from typing import Optional

COMMON_PORTS = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS/TLS",
    3389: "RDP",
}

HTTP_PREFIXES = (
    b"GET ", b"POST ", b"PUT ", b"PATCH ", b"DELETE ", b"HEAD ",
    b"OPTIONS ", b"CONNECT ", b"HTTP/",
)


def common_service(src_port: Optional[int], dst_port: Optional[int]) -> Optional[str]:
    """Return a well-known service name for either endpoint port."""
    if dst_port in COMMON_PORTS:
        return COMMON_PORTS[dst_port]
    if src_port in COMMON_PORTS:
        return COMMON_PORTS[src_port]
    return None


def looks_like_http(payload: bytes) -> bool:
    """Identify a visible HTTP start line without treating a port as proof."""
    sample = payload.lstrip()[:16].upper()
    return any(sample.startswith(prefix) for prefix in HTTP_PREFIXES)


def chart_category(protocol: str, transport: str) -> str:
    """Map detailed labels to exclusive dashboard chart categories."""
    if protocol == "DNS":
        return "DNS"
    if transport in {"TCP", "UDP", "ICMP"}:
        return transport
    return "Other"

