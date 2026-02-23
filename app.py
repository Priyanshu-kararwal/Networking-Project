import streamlit as st
from datetime import datetime
import os
import sys

sys.path.append('.')
import monitor

# ============================================================
# ICON DIRECTORY (YOUR PATH)
# ============================================================
ICON_DIR = r"D:/Priyanshu/main project/icon"

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Enterprise Network Monitoring Dashboard",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# WHITE ENTERPRISE THEME
# ============================================================
light_theme_css = """
<style>

body,
.main,
[data-testid="stAppViewContainer"]{
    background:#f5f7fb;
    color:#1e293b;
}

/* HEADER */
.noc-header{
    background:white;
    border-bottom:2px solid #2563eb;
    padding:1.5rem;
    margin-bottom:2rem;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

.header-top{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.header-title h1{
    color:#2563eb;
    margin:0;
}

.header-title p{
    color:#64748b;
}

.clock{
    font-weight:600;
    color:#2563eb;
}

.system-status{
    border:1px solid #22c55e;
    padding:0.4rem 1rem;
    border-radius:20px;
}

/* DEVICE CARD */
.device-card{
    background:white;
    border:1px solid #e2e8f0;
    border-radius:12px;
    padding:1.5rem;
    text-align:center;
    margin-bottom:1rem;
    transition:.3s;
}

.device-card:hover{
    box-shadow:0 4px 15px rgba(0,0,0,.1);
}

.device-card.online{
    border-top:4px solid #22c55e;
}

.device-card.offline{
    border-top:4px solid #ef4444;
}

.device-name{
    font-weight:600;
    margin-bottom:.6rem;
}

/* STATUS TABLE */
.status-row{
    display:grid;
    grid-template-columns:2fr 1fr 1fr 1fr 1fr;
    padding:1rem;
    background:white;
    border-bottom:1px solid #e2e8f0;
}

.status-table-header{
    display:grid;
    grid-template-columns:2fr 1fr 1fr 1fr 1fr;
    background:#2563eb;
    color:white;
    padding:1rem;
    font-weight:600;
}

.status-badge.online{
    background:#dcfce7;
    color:#166534;
    padding:.3rem .8rem;
    border-radius:15px;
}

.status-badge.offline{
    background:#fee2e2;
    color:#991b1b;
    padding:.3rem .8rem;
    border-radius:15px;
}

/* BUTTON */
.stButton>button{
    width:100%;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:6px;
}

</style>
"""

st.markdown(light_theme_css, unsafe_allow_html=True)

# Add CSS for icon sizing
icon_css = """
<style>
.device-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0.5rem;
}
.icon-img {
    width: 60px;
    height: 60px;
    object-fit: contain;
    display: block;
}
</style>
"""
st.markdown(light_theme_css + icon_css, unsafe_allow_html=True)

# ============================================================
# DEVICES
# ============================================================
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

device_layers = {
    "WAN/ISP Layer": ["MPLS-1","MPLS-2","ILL-1","ILL-2"],
    "Core Layer": ["Core Storage"],
    "Consolidation": ["Firewall","Backup Storage"],
    "Access Layer": ["AP-1","AP-2"],
    "End Devices": ["PC-1","PC-2","PC-3","PC-4"]
}

all_devices=[d for l in device_layers.values() for d in l]

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="noc-header">
<div class="header-top">
<div class="header-title">
<h1>🛰️ Enterprise Network Monitoring</h1>
<p>Real-Time Device Health Dashboard</p>
</div>
<div>
<span class="clock">{datetime.now().strftime("%H:%M:%S")}</span>
</div>
</div>
</div>
""",unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "device_states" not in st.session_state:
    st.session_state.device_states={d:True for d in all_devices}

device_states={}

# ============================================================
# DEVICE PANEL
# ============================================================
for layer,devices in device_layers.items():

    st.subheader(f"📍 {layer}")
    cols=st.columns(4)

    for i,device in enumerate(devices):

        with cols[i%4]:

            online=st.session_state.device_states[device]
            card_class="device-card online" if online else "device-card offline"

            icon_file=device_icons.get(device)
            icon_html=""

            if icon_file:
                icon_path=os.path.join(ICON_DIR,icon_file)
                if os.path.exists(icon_path):
                    icon_html=f"""
                    <div class="device-icon">
                        <img src="file:///{icon_path.replace('\\','/')}" alt="{device}" class="icon-img">
                    </div>
                    """

            st.markdown(
                f'<div class="{card_class}">{icon_html}<div class="device-name">{device}</div>',
                unsafe_allow_html=True
            )

            state=st.toggle(
                "",
                value=online,
                key=f"toggle_{device}"
            )

            st.session_state.device_states[device]=state
            device_states[device]=state

            badge="online" if state else "offline"
            text="🟢 ONLINE" if state else "🔴 OFFLINE"

            st.markdown(
                f'<div class="status-badge {badge}">{text}</div></div>',
                unsafe_allow_html=True
            )

# ============================================================
# TOPOLOGY
# ============================================================
st.subheader("📊 Network Topology")

diagram_img=monitor.get_network_diagram(device_states)

st.image(
    diagram_img,
    caption="Live Network Topology",
    use_column_width=True
)

# ============================================================
# METRICS
# ============================================================
online_count=sum(device_states.values())
offline_count=len(device_states)-online_count
health=(online_count/len(device_states))*100

c1,c2,c3,c4=st.columns(4)

c1.metric("Online Devices",online_count)
c2.metric("Offline Devices",offline_count)
c3.metric("Network Health",f"{health:.1f}%")
c4.metric("Last Updated",datetime.now().strftime("%H:%M:%S"))

# ============================================================
# STATUS TABLE
# ============================================================
st.markdown("""
<div class="status-table-header">
<div>Device</div>
<div>Status</div>
<div>Latency</div>
<div>Packet Loss</div>
<div>Health</div>
</div>
""",unsafe_allow_html=True)

for device in all_devices:

    online=device_states[device]

    st.markdown(f"""
    <div class="status-row">
    <div>{device}</div>
    <div><span class="status-badge {'online' if online else 'offline'}">
    {"Online" if online else "Offline"}
    </span></div>
    <div>{"5ms" if online else "-"}</div>
    <div>{"0%" if online else "100%"}</div>
    <div>{"100%" if online else "0%"}</div>
    </div>
    """,unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<hr>
<center>
Enterprise Network Monitoring Dashboard v1.0<br>
{datetime.now().strftime("%H:%M:%S")}
</center>
""",unsafe_allow_html=True)