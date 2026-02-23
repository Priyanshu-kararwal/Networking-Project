import streamlit as st
from datetime import datetime
import os
import sys
sys.path.append('.')
import monitor

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Enterprise Network Monitoring Dashboard",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM STYLING - DARK PROFESSIONAL NOC THEME
# ============================================================================
dark_theme_css = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: linear-gradient(135deg, #0f172a 0%, #1a202c 100%);
        color: #e2e8f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1a202c 100%);
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1a202c 100%);
    }
    
    /* Header Navbar */
    .noc-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border-bottom: 2px solid #22c55e;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-radius: 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    
    .header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .header-title h1 {
        font-size: 2.2em;
        font-weight: 700;
        color: #22c55e;
        margin: 0;
        text-shadow: 0 2px 10px rgba(34, 197, 94, 0.3);
        letter-spacing: 1px;
    }
    
    .header-title p {
        font-size: 0.95em;
        color: #cbd5e1;
        margin: 0.25rem 0 0 0;
        font-weight: 300;
    }
    
    .header-status {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .clock {
        font-size: 1.2em;
        color: #22c55e;
        font-weight: 600;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
    }
    
    .system-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(34, 197, 94, 0.1);
        border-radius: 20px;
        border: 1px solid #22c55e;
    }
    
    .status-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 10px #22c55e; }
        50% { box-shadow: 0 0 20px #22c55e; }
        100% { box-shadow: 0 0 10px #22c55e; }
    }
    
    /* Section Headers */
    .section-header {
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #334155;
    }
    
    .section-header h2 {
        font-size: 1.8em;
        color: #f1f5f9;
        margin-bottom: 0.25rem;
        font-weight: 700;
    }
    
    .section-header p {
        color: #94a3b8;
        font-size: 0.9em;
    }
    
    /* Device Control Cards */
    .device-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .device-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(34, 197, 94, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .device-card:hover::before {
        left: 100%;
    }
    
    .device-card:hover {
        border-color: #22c55e;
        background: linear-gradient(135deg, #1e293b 0%, #164e3a 100%);
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
        transform: translateY(-4px);
    }
    
    .device-card.online {
        border-top: 3px solid #22c55e;
    }
    
    .device-card.offline {
        border-top: 3px solid #ef4444;
        opacity: 0.7;
    }
    
    .device-icon {
        margin-bottom: 1rem;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .device-icon img {
        max-width: 70px;
        max-height: 70px;
        filter: drop-shadow(0 0 8px rgba(34, 197, 94, 0.3));
    }
    
    .device-name {
        font-size: 1.1em;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.8rem;
        letter-spacing: 0.5px;
    }
    
    .device-toggle {
        margin-bottom: 0.8rem;
    }
    
    .device-status-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 0.6rem;
        background: rgba(34, 197, 94, 0.1);
        border-radius: 8px;
        font-size: 0.9em;
        font-weight: 600;
    }
    
    .device-status-indicator.online {
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .device-status-indicator.offline {
        color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Status Overview Table */
    .status-table {
        margin-top: 1.5rem;
    }
    
    .status-table-header {
        display: grid;
        grid-template-columns: 2fr 1fr 1.5fr 1.5fr 1fr;
        gap: 1rem;
        padding: 1rem;
        background: #0f172a;
        border-radius: 8px 8px 0 0;
        border-bottom: 2px solid #22c55e;
        font-weight: 700;
        color: #22c55e;
        margin-bottom: 0;
    }
    
    .status-row {
        display: grid;
        grid-template-columns: 2fr 1fr 1.5fr 1.5fr 1fr;
        gap: 1rem;
        padding: 1rem;
        background: #1e293b;
        border-bottom: 1px solid #334155;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .status-row:hover {
        background: #334155;
        border-left: 3px solid #22c55e;
        padding-left: calc(1rem - 3px);
    }
    
    .status-row:last-child {
        border-radius: 0 0 8px 8px;
    }
    
    .status-cell {
        color: #e2e8f0;
        font-size: 0.95em;
    }
    
    .status-cell.device-name {
        font-weight: 600;
        color: #f1f5f9;
    }
    
    .status-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        text-align: center;
        width: fit-content;
    }
    
    .status-badge.online {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid #22c55e;
    }
    
    .status-badge.offline {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    
    .status-badge.warning {
        background: rgba(250, 204, 21, 0.2);
        color: #facc15;
        border: 1px solid #facc15;
    }
    
    /* Network Topology Section */
    .topology-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        min-height: 400px;
    }
    
    .topology-svg {
        display: block;
        margin: 0 auto;
        max-width: 100%;
    }
    
    /* Responsive Grid */
    @media (max-width: 1200px) {
        .device-grid {
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 1rem !important;
        }
    }
    
    @media (max-width: 768px) {
        .device-grid {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 1rem !important;
        }
        
        .status-table-header,
        .status-row {
            grid-template-columns: 1fr 1fr 1fr !important;
            gap: 0.5rem !important;
        }
        
        .header-status {
            flex-direction: column;
            gap: 1rem;
            width: 100%;
        }
    }
    
    @media (max-width: 480px) {
        .device-grid {
            display: grid !important;
            grid-template-columns: 1fr !important;
            gap: 1rem !important;
        }
        
        .status-table-header,
        .status-row {
            grid-template-columns: 1fr !important;
            gap: 0.5rem !important;
            padding: 0.75rem !important;
        }
        
        .noc-header {
            padding: 1rem;
        }
        
        .header-title h1 {
            font-size: 1.5em;
        }
    }
    
    /* Streamlit default overrides */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.5);
    }
    
    .stToggle {
        margin: 0.5rem 0;
    }
    
    .stMetric {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
    }
</style>
"""

st.markdown(dark_theme_css, unsafe_allow_html=True)

# ============================================================================
# DEVICE CONFIGURATION
# ============================================================================
device_icons = {
    "MPLS-1": "mpls.png",
    "MPLS-2": "mpls.png",
    "ILL-1": "ill.png",
    "ILL-2": "ill.png",
    "Core Storage": "server.png",
    "Firewall": "firewall.png",
    "Backup Storage": "server.png",
    "AP-1": "wifi.png",
    "AP-2": "wifi.png",
    "PC-1": "pc.png",
    "PC-2": "pc.png",
    "PC-3": "pc.png",
    "PC-4": "pc.png"
}

# Organize devices by layer
device_layers = {
    "WAN/ISP Layer": ["MPLS-1", "MPLS-2", "ILL-1", "ILL-2"],
    "Core Layer": ["Core Storage"],
    "Consolidation": ["Firewall", "Backup Storage"],
    "Access Layer": ["AP-1", "AP-2"],
    "End Devices": ["PC-1", "PC-2", "PC-3", "PC-4"]
}

# Flatten all devices
all_devices = [dev for layer in device_layers.values() for dev in layer]

# ============================================================================
# HEADER SECTION
# ============================================================================
header_html = f"""
<div class="noc-header">
    <div class="header-top">
        <div class="header-title">
            <h1>🛰️ Enterprise Network Monitoring</h1>
            <p>Real-Time Device Health Dashboard</p>
        </div>
        <div class="header-status">
            <div class="clock" id="live-clock">00:00:00</div>
            <div class="system-status">
                <div class="status-dot"></div>
                <span>System Active</span>
            </div>
        </div>
    </div>
</div>

<script>
    function updateClock() {{
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        document.getElementById('live-clock').textContent = hours + ':' + minutes + ':' + seconds;
    }}
    updateClock();
    setInterval(updateClock, 1000);
</script>
"""

st.markdown(header_html, unsafe_allow_html=True)

# ============================================================================
# DEVICE CONTROL PANEL
# ============================================================================
st.markdown("""
<div class="section-header">
    <h2>🎮 Device Control Panel</h2>
    <p>Manage and monitor all network devices</p>
</div>
""", unsafe_allow_html=True)

# Session state for device states
if 'device_states' not in st.session_state:
    st.session_state.device_states = {dev: True for dev in all_devices}

# Create responsive grid for devices
cols_per_row = 4
device_states = {}

for layer_name, devices in device_layers.items():
    st.markdown(f"<h3 style='color: #cbd5e1; margin-top: 1.5rem; margin-bottom: 1rem; font-weight: 600;'>📍 {layer_name}</h3>", unsafe_allow_html=True)
    
    cols = st.columns(min(len(devices), cols_per_row))
    
    for idx, device in enumerate(devices):
        col_idx = idx % len(cols)
        
        with cols[col_idx]:
            # Device card
            is_online = st.session_state.device_states[device]
            card_class = "device-card online" if is_online else "device-card offline"
            
            card_html_start = f'<div class="{card_class}">'
            
            # Icon
            icon_file = device_icons.get(device)
            icon_html = ""
            if icon_file:
                icon_path = f"icon/{icon_file}"
                if os.path.exists(icon_path):
                    icon_html = f'<div class="device-icon"><img src="file://{os.path.abspath(icon_path)}" alt="{device}"></div>'
            
            # Device name
            name_html = f'<div class="device-name">{device}</div>'
            
            st.markdown(card_html_start + icon_html + name_html, unsafe_allow_html=True)
            
            # Toggle switch
            state = st.toggle(
                label=f"Status##toggle_{device}",
                value=st.session_state.device_states[device],
                key=f"toggle_{device}"
            )
            st.session_state.device_states[device] = state
            device_states[device] = state
            
            # Status indicator
            status_color = "online" if state else "offline"
            status_text = "🟢 ONLINE" if state else "🔴 OFFLINE"
            
            status_html = f"""
            <div class="device-status-indicator {status_color}">
                {status_text}
            </div>
            </div>
            """
            st.markdown(status_html, unsafe_allow_html=True)

# ============================================================================
# NETWORK TOPOLOGY DIAGRAM
# ============================================================================
st.markdown("""
<div class="section-header">
    <h2>📊 Network Topology Diagram</h2>
    <p>Visual representation of network hierarchy and connections</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="topology-container">', unsafe_allow_html=True)
diagram_img = monitor.get_network_diagram(device_states)
st.image(diagram_img, caption="Live Network Topology - Click toggles to simulate device failures", use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# DEVICE STATUS OVERVIEW (TABLE)
# ============================================================================
st.markdown("""
<div class="section-header">
    <h2>📋 Device Status Overview</h2>
    <p>Comprehensive device health metrics and statistics</p>
</div>
""", unsafe_allow_html=True)

# Calculate metrics
online_count = sum(1 for state in device_states.values() if state)
offline_count = len(device_states) - online_count
health_percent = (online_count / len(device_states)) * 100

# Metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🟢 Online Devices", online_count, f"{online_count}/{len(device_states)}")
with col2:
    st.metric("🔴 Offline Devices", offline_count, f"{offline_count}/{len(device_states)}")
with col3:
    st.metric("📊 Network Health", f"{health_percent:.1f}%", "All Systems" if health_percent == 100 else "Degraded")
with col4:
    st.metric("⏱️ Last Updated", datetime.now().strftime("%H:%M:%S"), "Real-time")

# Status table
st.markdown('<div class="status-table"><div class="status-table-header"><div>Device Name</div><div>Status</div><div>Latency</div><div>Packet Loss</div><div>Health %</div></div>', unsafe_allow_html=True)

for device in all_devices:
    is_online = device_states[device]
    status_badge = "🟢 Online" if is_online else "🔴 Offline"
    latency = "5ms" if is_online else "—"
    packet_loss = "0.0%" if is_online else "100%"
    health = "100%" if is_online else "0%"
    
    row_html = f"""
    <div class="status-row">
        <div class="status-cell device-name">{device}</div>
        <div class="status-cell"><span class="status-badge {'online' if is_online else 'offline'}">{status_badge}</span></div>
        <div class="status-cell">{latency}</div>
        <div class="status-cell">{packet_loss}</div>
        <div class="status-cell">{health}</div>
    </div>
    """
    st.markdown(row_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
footer_html = """
<div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #334155; text-align: center; color: #64748b; font-size: 0.9em;">
    <p>Enterprise Network Monitoring Dashboard v1.0 | Last Refresh: <span id="footer-time">-</span></p>
    <p style="margin-top: 0.5rem; font-size: 0.85em;">© 2026 Network Operations Center</p>
</div>

<script>
    document.getElementById('footer-time').textContent = new Date().toLocaleTimeString();
</script>
"""
st.markdown(footer_html, unsafe_allow_html=True)