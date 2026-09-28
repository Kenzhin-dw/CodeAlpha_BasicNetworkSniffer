from sniffer.statistics import calculate_statistics, packets_over_time


PACKETS = [
    {
        "timestamp": "2026-01-01T10:00:00+00:00",
        "src_ip": "192.0.2.1",
        "dst_ip": "198.51.100.1",
        "protocol": "HTTPS/TLS",
        "transport": "TCP",
        "src_port": 51000,
        "dst_port": 443,
        "length": 100,
    },
    {
        "timestamp": "2026-01-01T10:00:00.500+00:00",
        "src_ip": "192.0.2.1",
        "dst_ip": "203.0.113.53",
        "protocol": "DNS",
        "transport": "UDP",
        "src_port": 53000,
        "dst_port": 53,
        "length": 60,
    },
    {
        "timestamp": "2026-01-01T10:00:02+00:00",
        "src_ip": "198.51.100.2",
        "dst_ip": "192.0.2.1",
        "protocol": "ICMP",
        "transport": "ICMP",
        "src_port": None,
        "dst_port": None,
        "length": 80,
    },
]


def test_statistics_counts_and_rankings() -> None:
    stats = calculate_statistics(PACKETS)

    assert stats["total_packets"] == 3
    assert stats["total_bytes"] == 240
    assert stats["average_packet_size"] == 80
    assert stats["tcp_count"] == 1
    assert stats["udp_count"] == 1
    assert stats["icmp_count"] == 1
    assert stats["dns_count"] == 1
    assert stats["top_source_ips"][0] == ("192.0.2.1", 2)
    assert stats["protocol_categories"]["DNS"] == 1


def test_statistics_empty_input() -> None:
    stats = calculate_statistics([])
    assert stats["total_packets"] == 0
    assert stats["average_packet_size"] == 0
    assert stats["protocol_categories"] == {
        "TCP": 0, "UDP": 0, "ICMP": 0, "DNS": 0, "Other": 0
    }


def test_packets_over_time_groups_seconds() -> None:
    timeline = packets_over_time(PACKETS)
    assert timeline["packets"].tolist() == [2, 0, 1]

