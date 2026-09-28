"""Streamlit dashboard for authorized local network traffic monitoring."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st

from sniffer.capture import CaptureManager, CaptureState, SCAPY_IMPORT_ERROR
from sniffer.statistics import calculate_statistics, packets_over_time
from utils.export import packets_to_csv

st.set_page_config(
    page_title="Network Packet Sniffer",
    page_icon="🌐",
    layout="wide",
)


@st.cache_resource
def get_capture_manager() -> CaptureManager:
    """Persist one capture controller across Streamlit script reruns."""
    return CaptureManager(capacity=10_000)


def format_bytes(value: int) -> str:
    size = float(value)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"


def apply_filters(
    packets: list[dict[str, Any]],
    protocols: list[str],
    source_filter: str,
    destination_filter: str,
) -> list[dict[str, Any]]:
    """Apply non-destructive, case-insensitive dashboard filters."""
    source = source_filter.strip().lower()
    destination = destination_filter.strip().lower()
    return [
        packet
        for packet in packets
        if (not protocols or packet.get("protocol") in protocols)
        and (not source or source in str(packet.get("src_ip", "")).lower())
        and (not destination or destination in str(packet.get("dst_ip", "")).lower())
    ]


def render_ranked(title: str, values: list[tuple[Any, int]]) -> None:
    st.subheader(title)
    if not values:
        st.caption("No packet data yet.")
        return
    frame = pd.DataFrame(values, columns=["Value", "Packets"]).set_index("Value")
    st.bar_chart(frame, horizontal=True)


def render_dashboard(
    manager: CaptureManager,
    protocol_filter: list[str],
    source_filter: str,
    destination_filter: str,
    maximum_packets: int,
) -> None:
    packets = manager.snapshot()
    filtered = apply_filters(packets, protocol_filter, source_filter, destination_filter)
    displayed = filtered[-maximum_packets:]
    stats = calculate_statistics(filtered)

    metric_columns = st.columns(5)
    metric_columns[0].metric("Total Packets", stats["total_packets"])
    metric_columns[1].metric("TCP", stats["tcp_count"])
    metric_columns[2].metric("UDP", stats["udp_count"])
    metric_columns[3].metric("ICMP", stats["icmp_count"])
    metric_columns[4].metric("Total Traffic", format_bytes(stats["total_bytes"]))

    st.subheader("Live Packets")
    if not displayed:
        st.info("No packets match the current filters. Start capture or generate normal local traffic.")
    else:
        table_columns = [
            "timestamp", "src_ip", "dst_ip", "protocol", "src_port",
            "dst_port", "length",
        ]
        frame = pd.DataFrame(displayed)[table_columns].rename(
            columns={
                "timestamp": "Timestamp",
                "src_ip": "Source",
                "dst_ip": "Destination",
                "protocol": "Protocol",
                "src_port": "Source Port",
                "dst_port": "Destination Port",
                "length": "Length",
            }
        )
        st.dataframe(frame.iloc[::-1], use_container_width=True, hide_index=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Protocol Distribution")
        protocol_frame = pd.DataFrame(
            {"Packets": stats["protocol_categories"]}
        ).reindex(["TCP", "UDP", "ICMP", "DNS", "Other"])
        st.bar_chart(protocol_frame)
    with right:
        st.subheader("Capture Summary")
        st.metric("Average Packet Size", format_bytes(round(stats["average_packet_size"])))
        st.metric("DNS Packets", stats["dns_count"])
        st.caption("Counts and charts reflect the active dashboard filters.")

    left, right = st.columns(2)
    with left:
        render_ranked("Top Source IPs", stats["top_source_ips"])
        render_ranked("Top Source Ports", stats["top_source_ports"])
    with right:
        render_ranked("Top Destination IPs", stats["top_destination_ips"])
        render_ranked("Top Destination Ports", stats["top_destination_ports"])

    st.subheader("Packet Timeline")
    timeline = packets_over_time(filtered)
    if timeline.empty:
        st.caption("Timeline will appear after packets are captured.")
    else:
        st.line_chart(timeline.set_index("timestamp"))

    st.subheader("Packet Details")
    if displayed:
        newest_first = list(reversed(displayed))
        options = range(len(newest_first))
        selected = st.selectbox(
            "Select a packet",
            options,
            format_func=lambda index: (
                f"{newest_first[index]['timestamp']} — "
                f"{newest_first[index]['src_ip']} → {newest_first[index]['dst_ip']} "
                f"({newest_first[index]['protocol']})"
            ),
        )
        details = newest_first[selected]
        safe_details = {key: value for key, value in details.items() if key != "payload_preview"}
        st.json(safe_details)
        if "payload_preview" in details:
            st.warning("Optional sanitized payload preview is enabled for this captured packet.")
            st.code(details["payload_preview"] or "(no payload)")
    else:
        st.caption("Select packet details after traffic is captured.")

    st.download_button(
        "Download filtered metadata as CSV",
        data=packets_to_csv(filtered),
        file_name=f"captured_packets_{datetime.now():%Y%m%d_%H%M%S}.csv",
        mime="text/csv",
        disabled=not filtered,
        help="Exports metadata only; raw packet payload is excluded.",
    )


def main() -> None:
    manager = get_capture_manager()
    status = manager.status()

    st.title("NETWORK PACKET SNIFFER")
    st.caption("Real-time Network Traffic Monitoring")
    st.info("Use only on computers and networks you own or are authorized to inspect.", icon="🔒")

    with st.sidebar:
        st.header("Capture Controls")
        interfaces = manager.interfaces()
        selected_interface = st.selectbox(
            "Network Interface",
            interfaces,
            index=0 if interfaces else None,
            placeholder="No interfaces available",
            disabled=status.state == CaptureState.RUNNING or not interfaces,
        )
        preview_enabled = st.checkbox(
            "Optional sanitized payload preview",
            value=False,
            disabled=status.state == CaptureState.RUNNING,
            help="Disabled by default. Stores at most 64 sanitized bytes per new packet.",
        )
        st.write(f"**Capture Status:** {status.state.value}")
        if status.interface:
            st.caption(f"Interface: {status.interface}")

        start_column, stop_column = st.columns(2)
        if start_column.button(
            "Start Capture",
            type="primary",
            disabled=status.state == CaptureState.RUNNING or not interfaces,
            use_container_width=True,
        ):
            if manager.start(selected_interface or "", preview_enabled):
                st.rerun()
        if stop_column.button(
            "Stop Capture",
            disabled=status.state != CaptureState.RUNNING,
            use_container_width=True,
        ):
            manager.stop()
            st.rerun()
        if st.button("Clear Data", use_container_width=True):
            manager.clear()
            st.rerun()

        if SCAPY_IMPORT_ERROR:
            st.error("Scapy could not be imported. Install the project requirements.")
        if status.error:
            st.error(status.error)
        if not interfaces:
            st.warning("No capture interfaces found. Install Npcap and restart the application.")

        st.divider()
        st.header("Display Filters")
        baseline_protocols = {
            "TCP", "UDP", "ICMP", "DNS", "HTTP", "HTTPS/TLS", "FTP-DATA",
            "FTP", "SSH", "TELNET", "SMTP", "DHCP", "POP3", "IMAP", "RDP", "Other",
        }
        observed_protocols = {
            str(packet.get("protocol")) for packet in manager.snapshot() if packet.get("protocol")
        }
        protocol_filter = st.multiselect(
            "Protocol Filter",
            sorted(baseline_protocols | observed_protocols),
        )
        source_filter = st.text_input("Source IP Filter", placeholder="e.g. 192.168.")
        destination_filter = st.text_input("Destination IP Filter", placeholder="e.g. 8.8.8.8")
        maximum_packets = st.slider("Maximum Displayed Packets", 25, 1000, 250, 25)
        auto_refresh = st.checkbox("Auto Refresh", value=True)
        refresh_seconds = st.select_slider("Refresh Interval", [1, 2, 3, 5, 10], value=2)

    if auto_refresh:
        @st.fragment(run_every=f"{refresh_seconds}s")
        def live_fragment() -> None:
            render_dashboard(
                manager, protocol_filter, source_filter, destination_filter, maximum_packets
            )

        live_fragment()
    else:
        render_dashboard(manager, protocol_filter, source_filter, destination_filter, maximum_packets)

    st.caption(
        "Raw payload is not captured by default. HTTPS/TLS content remains encrypted and is not decrypted."
    )


if __name__ == "__main__":
    main()
