import matplotlib.pyplot as plt

colors_map = {
    "runtime": "green",
    "process": "blue",
    "maintenance": "yellow",
    "other": "red"
}

fig, ax = plt.subplots(figsize=(10, 1))
start = raw_data[0]["ts"]

for seg in segments:
    x_start = (seg["start_ts"] - start) / 60  # minutes from start
    x_width = (seg["end_ts"] - seg["start_ts"]) / 60
    color = "green"
    if seg["status"] == "downtime":
        reason = input(f"Enter reason for downtime from {seg['start_ts']} to {seg['end_ts']}: ")
        color = colors_map.get(reason, "gray")
    ax.barh(0, x_width, left=x_start, height=0.5, color=color)

ax.set_yticks([])
ax.set_xlabel("Minutes from Start")
plt.title("Machine Runtime/Downtime Segments")
plt.show()
    