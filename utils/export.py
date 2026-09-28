"""Safe CSV export for packet metadata."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

EXPORT_COLUMNS = [
    "timestamp", "src_ip", "dst_ip", "protocol", "src_port",
    "dst_port", "length", "payload_length",
]


def packets_to_csv(packets: list[dict[str, Any]]) -> bytes:
    """Serialize only approved metadata columns to UTF-8 CSV bytes."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=EXPORT_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for packet in packets:
        writer.writerow({column: packet.get(column, "") for column in EXPORT_COLUMNS})
    return buffer.getvalue().encode("utf-8")


def export_packets_csv(packets: list[dict[str, Any]], path: Path) -> Path:
    """Write safe metadata CSV to an explicitly supplied path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(packets_to_csv(packets))
    return path
