from matplotlib.figure import Figure
from backend.server.mongo import fetch_graphdata
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_production_data(parent_frame):
    data3 = fetch_graphdata()
 
    if not isinstance(data3, dict):
        print("No valid data found.")
        return

    categories = ["Run Time", "Process Downtime", "Maintenance DT", "Other Downtime"]
    values = [
        data3.get("run_time", 0),
        data3.get("process_downtime", 0),
        data3.get("maintenance_dt", 0),
        data3.get("other_downtime", 0)
    ]

    fig = Figure(figsize=(10, 2), dpi=100)
    ax = fig.add_subplot(111)

    left = 0
    colors = ["#2cf14d", "#567cdb", "#93f8f0", "#f7b9c0"]
    for i, value in enumerate(values):
        ax.barh("Downtime", value, left=left, color=colors[i], label=categories[i])
        left += value

    ax.set_xlim(0, sum(values) + 10)
    ax.set_yticks([])
    ax.set_title("Downtime Breakdown")
    ax.legend(loc="upper right", fontsize=8)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
