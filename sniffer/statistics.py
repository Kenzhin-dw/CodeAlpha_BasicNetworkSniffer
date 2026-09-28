"""Lightweight traffic statistics over parsed packet dictionaries."""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

import pandas as pd

from .protocols import chart_category


def _top(values: Iterable[Any], limit: int = 5) -> list[tuple[Any, int]]:
    return Counter(value for value in values if value not in (None, "")).most_common(limit)


def calculate_statistics(packets: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate dashboard-ready counts while handling an empty capture."""
    total = len(packets)
    total_bytes = sum(int(packet.get("length", 0) or 0) for packet in packets)
    transports = Counter(packet.get("transport", "Other") for packet in packets)
    protocols = Counter(packet.get("protocol", "Other") for packet in packets)
    categories = Counter(
        chart_category(str(packet.get("protocol", "Other")), str(packet.get("transport", "Other")))
        for packet in packets
    )
    for category in ("TCP", "UDP", "ICMP", "DNS", "Other"):
        categories.setdefault(category, 0)

    return {
        "total_packets": total,
        "total_bytes": total_bytes,
        "average_packet_size": (total_bytes / total) if total else 0.0,
        "tcp_count": transports["TCP"],
        "udp_count": transports["UDP"],
        "icmp_count": transports["ICMP"],
        "dns_count": protocols["DNS"],
        "packets_per_protocol": dict(protocols),
        "protocol_categories": dict(categories),
        "top_source_ips": _top(packet.get("src_ip") for packet in packets),
        "top_destination_ips": _top(packet.get("dst_ip") for packet in packets),
        "top_source_ports": _top(packet.get("src_port") for packet in packets),
        "top_destination_ports": _top(packet.get("dst_port") for packet in packets),
    }


def packets_over_time(packets: list[dict[str, Any]], frequency: str = "1s") -> pd.DataFrame:
    """Return timestamp/count points grouped into a small time interval."""
    if not packets:
        return pd.DataFrame(columns=["timestamp", "packets"])
    frame = pd.DataFrame({"timestamp": [packet.get("timestamp") for packet in packets]})
    frame["timestamp"] = pd.to_datetime(
        frame["timestamp"], errors="coerce", utc=True, format="mixed"
    )
    frame = frame.dropna()
    if frame.empty:
        return pd.DataFrame(columns=["timestamp", "packets"])
    result = frame.set_index("timestamp").resample(frequency).size().rename("packets").reset_index()
    return result
