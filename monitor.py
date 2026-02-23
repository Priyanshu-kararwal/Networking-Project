import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button
import os


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


fig, ax = plt.subplots(figsize=(14,9))
plt.subplots_adjust(right=0.78)

ax.set_xlim(0,10)
ax.set_ylim(0,10)
ax.axis('off')

def draw_network():

    ax.clear()
    ax.set_xlim(0,10)
    ax.set_ylim(0,10)
    ax.axis('off')

    for a,b in connections:
        if device_state[a] and device_state[b]:
            x1,y1 = pos[a]
            x2,y2 = pos[b]

            ax.plot(
                [x1,x2],
                [y1,y2],
                color="black",
                linewidth=2,
                zorder=1
            )

    # ---------- DEVICE ICONS ----------
    for dev,icon in devices.items():

        x,y = pos[dev]
        path = os.path.join(ICON_PATH,icon)

        if os.path.exists(path):
            img = mpimg.imread(path)
            ax.imshow(
                img,
                extent=(x-ICON_SIZE,
                        x+ICON_SIZE,
                        y-ICON_SIZE,
                        y+ICON_SIZE),
                zorder=3
            )

        status = "ON" if device_state[dev] else "OFF"
        color = "green" if device_state[dev] else "red"

        # PCs → label BELOW
        if "PC" in dev:
            ax.text(
                x,
                y-0.85,
                f"{dev} ({status})",
                ha="center",
                fontsize=11,
                fontweight="bold",
                color=color,
                zorder=5
            )

        # Network devices → label BESIDE
        else:
            ax.text(
                x+0.7,
                y,
                f"{dev} ({status})",
                va="center",
                fontsize=11,
                fontweight="bold",
                color=color,
                zorder=5
            )

    ax.set_title(
        "Enterprise Network Failure Simulation Dashboard",
        fontsize=18,
        fontweight="bold"
    )

    plt.draw()

draw_network()


# TOGGLE BUTTONS
buttons = {}
y_pos = 0.92

def toggle_device(device):

    def action(event):
        device_state[device] = not device_state[device]
        draw_network()

    return action

for dev in devices:
    ax_btn = plt.axes([0.82, y_pos, 0.15, 0.04])
    btn = Button(ax_btn, dev)
    btn.on_clicked(toggle_device(dev))
    buttons[dev] = btn
    y_pos -= 0.055

plt.show()