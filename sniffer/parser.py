"""Convert Scapy packets into privacy-conscious structured metadata."""

from __future__ import annotations

from datetime import datetime
import string
from typing import Any, Optional

from scapy.layers.dns import DNS
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.layers.inet6 import IPv6, _ICMPv6
from scapy.packet import Packet, Raw

from .protocols import common_service, looks_like_http

MAX_PREVIEW_LENGTH = 64


def _sanitize_payload(raw: bytes, limit: int = MAX_PREVIEW_LENGTH) -> str:
    """Return a bounded printable preview; non-printable bytes become dots."""
    allowed = set(string.printable) - {"\r", "\n", "\t", "\x0b", "\x0c"}
    text = "".join(chr(byte) if chr(byte) in allowed else "." for byte in raw[:limit])
    return text + ("..." if len(raw) > limit else "")


def _timestamp(packet: Packet) -> str:
    try:
        return datetime.fromtimestamp(float(packet.time)).astimezone().isoformat(timespec="milliseconds")
    except (AttributeError, OSError, TypeError, ValueError):
        return datetime.now().astimezone().isoformat(timespec="milliseconds")


def parse_packet(packet: Packet, include_payload_preview: bool = False) -> Optional[dict[str, Any]]:
    """Parse one IPv4/IPv6 packet, returning None for unsupported frames.

    Full payload bytes are never returned. The optional preview is sanitized
    and capped at 64 bytes.
    """
    try:
        if packet.haslayer(IP):
            ip_layer = packet[IP]
            ip_version = 4
        elif packet.haslayer(IPv6):
            ip_layer = packet[IPv6]
            ip_version = 6
        else:
            return None

        src_port: Optional[int] = None
        dst_port: Optional[int] = None
        tcp_flags = ""
        transport = "Other"

        if packet.haslayer(TCP):
            layer = packet[TCP]
            src_port, dst_port = int(layer.sport), int(layer.dport)
            tcp_flags = str(layer.flags)
            transport = "TCP"
        elif packet.haslayer(UDP):
            layer = packet[UDP]
            src_port, dst_port = int(layer.sport), int(layer.dport)
            transport = "UDP"
        elif packet.haslayer(ICMP) or packet.haslayer(_ICMPv6):
            transport = "ICMP"

        payload = bytes(packet[Raw].load) if packet.haslayer(Raw) else b""
        service = common_service(src_port, dst_port)

        if packet.haslayer(DNS):
            protocol = "DNS"
        elif transport == "ICMP":
            protocol = "ICMP"
        elif transport == "TCP" and looks_like_http(payload):
            protocol = "HTTP"
        elif transport == "TCP" and service == "HTTPS/TLS":
            protocol = "HTTPS/TLS"
        elif service:
            protocol = service
        else:
            protocol = transport

        result: dict[str, Any] = {
            "timestamp": _timestamp(packet),
            "src_ip": str(ip_layer.src),
            "dst_ip": str(ip_layer.dst),
            "protocol": protocol,
            "transport": transport,
            "src_port": src_port,
            "dst_port": dst_port,
            "length": len(packet),
            "ip_version": ip_version,
            "tcp_flags": tcp_flags,
            "summary": packet.summary(),
            "payload_present": bool(payload),
            "payload_length": len(payload),
        }
        if include_payload_preview:
            result["payload_preview"] = _sanitize_payload(payload) if payload else ""
        return result
    except (AttributeError, IndexError, TypeError, ValueError):
        return None

