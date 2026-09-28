import csv
import io

from utils.export import EXPORT_COLUMNS, packets_to_csv


def test_csv_contains_only_approved_metadata() -> None:
    packets = [{
        "timestamp": "2026-01-01T00:00:00+00:00",
        "src_ip": "192.0.2.1",
        "dst_ip": "198.51.100.1",
        "protocol": "TCP",
        "src_port": 12345,
        "dst_port": 443,
        "length": 64,
        "payload_length": 10,
        "payload_preview": "must-not-export",
        "unapproved": "must-not-export",
    }]

    text = packets_to_csv(packets).decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text)))

    assert list(rows[0].keys()) == EXPORT_COLUMNS
    assert rows[0]["src_ip"] == "192.0.2.1"
    assert "must-not-export" not in text


def test_empty_export_has_header() -> None:
    text = packets_to_csv([]).decode("utf-8")
    assert text.strip() == ",".join(EXPORT_COLUMNS)

