
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from io import BytesIO
from PIL import Image


ICON_PATH = "icon"

devices = {
    "MPLS-1":"mpls.png",
    "MPLS-2":"mpls.png",

    "ILL-1":"ill.png",
    "ILL-2":"ill.png",

    "Core Storage":"server.png",
    "Firewall":"firewall.png",
    "Backup Storage":"server.png",

    "AP-1":"wifi.png",
    "AP-2":"wifi.png",

    "PC-1":"pc.png",
    "PC-2":"pc.png",
    "PC-3":"pc.png",
    "PC-4":"pc.png"
}

device_state = {d: True for d in devices}


pos = {

"MPLS-1":(2,9),
"MPLS-2":(8,9),

"ILL-1":(2,7.5),
"ILL-2":(8,7.5),

"Core Storage":(5,6),

"Firewall":(5,4.5),

"Backup Storage":(5,3),

"AP-1":(3,1.8),
"AP-2":(7,1.8),

"PC-1":(2,0.6),
"PC-2":(4,0.6),
"PC-3":(6,0.6),
"PC-4":(8,0.6)
}


connections = [

("MPLS-1","Core Storage"),
("MPLS-2","Core Storage"),

("ILL-1","Core Storage"),
("ILL-2","Core Storage"),

("Core Storage","Firewall"),
("Firewall","Backup Storage"),

("Backup Storage","AP-1"),
("Backup Storage","AP-2"),

("AP-1","PC-1"),
("AP-1","PC-2"),

("AP-2","PC-3"),
("AP-2","PC-4"),
]

ICON_SIZE = 0.45



def get_network_diagram(device_state_override=None):
    """
    Draw the network diagram and return as a PIL Image.
    Optionally override device_state with a provided dict.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.08)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    state = device_state.copy()
    if device_state_override:
        state.update(device_state_override)

    for a, b in connections:
        if state[a] and state[b]:
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            ax.plot(
                [x1, x2],
                [y1, y2],
                color="#222",
                linewidth=2.5,
                zorder=1
            )

    for dev, icon in devices.items():
        x, y = pos[dev]
        path = os.path.join(ICON_PATH, icon)
        if os.path.exists(path):
            img = mpimg.imread(path)
            ax.imshow(
                img,
                extent=(x-ICON_SIZE, x+ICON_SIZE, y-ICON_SIZE, y+ICON_SIZE),
                zorder=3
            )
        status = "ON" if state[dev] else "OFF"
        color = "#388e3c" if state[dev] else "#c62828"
        if "PC" in dev:
            ax.text(
                x, y-0.85, f"{dev} ({status})",
                ha="center", fontsize=11, fontweight="bold",
                color=color, zorder=5
            )
        else:
            ax.text(
                x+0.7, y, f"{dev} ({status})",
                va="center", fontsize=11, fontweight="bold",
                color=color, zorder=5
            )

    ax.set_title(
        "Enterprise Network Failure Simulation Dashboard",
        fontsize=16, fontweight="bold"
    )

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)