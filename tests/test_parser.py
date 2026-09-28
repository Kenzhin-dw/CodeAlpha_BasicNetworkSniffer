from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.layers.inet6 import IPv6
from scapy.packet import Raw

from sniffer.parser import parse_packet
from sniffer.capture import CaptureManager


def test_parse_ipv4_tcp_http_metadata_without_preview() -> None:
    packet = (
        IP(src="192.0.2.10", dst="198.51.100.20")
        / TCP(sport=51515, dport=80, flags="PA")
        / Raw(load=b"GET / HTTP/1.1\r\nHost: example.test\r\n\r\n")
    )

    result = parse_packet(packet)

    assert result is not None
    assert result["src_ip"] == "192.0.2.10"
    assert result["dst_ip"] == "198.51.100.20"
    assert result["protocol"] == "HTTP"
    assert result["transport"] == "TCP"
    assert result["src_port"] == 51515
    assert result["dst_port"] == 80
    assert result["ip_version"] == 4
    assert result["payload_present"] is True
    assert result["payload_length"] > 0
    assert "payload_preview" not in result


def test_preview_is_optional_bounded_and_sanitized() -> None:
    packet = IP() / TCP(sport=1, dport=2) / Raw(load=b"secret\x00" + b"x" * 100)

    result = parse_packet(packet, include_payload_preview=True)

    assert result is not None
    assert result["payload_preview"].startswith("secret.")
    assert result["payload_preview"].endswith("...")
    assert len(result["payload_preview"]) <= 67


def test_parse_dns_before_port_only_classification() -> None:
    packet = IP(src="203.0.113.2", dst="203.0.113.53") / UDP(sport=53000, dport=53) / DNS(
        rd=1, qd=DNSQR(qname="example.com")
    )

    result = parse_packet(packet)

    assert result is not None
    assert result["protocol"] == "DNS"
    assert result["transport"] == "UDP"


def test_parse_icmp_and_ipv6() -> None:
    icmp = parse_packet(IP(src="192.0.2.1", dst="192.0.2.2") / ICMP())
    ipv6 = parse_packet(IPv6(src="2001:db8::1", dst="2001:db8::2") / UDP(sport=1, dport=2))

    assert icmp is not None and icmp["protocol"] == "ICMP"
    assert ipv6 is not None and ipv6["ip_version"] == 6


def test_non_ip_packet_is_ignored() -> None:
    assert parse_packet(Raw(load=b"not an IP packet")) is None


def test_interface_address_filter_excludes_windows_link_local() -> None:
    assert CaptureManager._has_usable_address("10.0.0.5") is True
    assert CaptureManager._has_usable_address("127.0.0.1") is True
    assert CaptureManager._has_usable_address("169.254.20.10") is False
    assert CaptureManager._has_usable_address("No IP address") is False
