from backend.server.mongo import get_mongo_connection
import matplotlib.pyplot as plt

def get_pie_colors():
    return ["#2cf14d", "#7e96d3", "#93f8f0", "#f7b9c0"]

def draw_pie_chart():
    db = get_mongo_connection()
    collection = db["graphdata"]

    # Fetch only one document since you mentioned it's a single document
    data = collection.find_one({}, {"_id": 0, "run_time": 1, "process_downtime": 1, "maintenance_dt": 1, "other_downtime": 1})
    
    if not data:
        return None

    labels = ["Running", "Process Downtime", "Maintenance", "Other Downtime"]
    values = [
        data.get("run_time", 0),
        data.get("process_downtime", 0),
        data.get("maintenance_dt", 0),
        data.get("other_downtime", 0)
    ]
    colors = get_pie_colors()

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(values)])
    ax.set_title("Machine Status")
    ax.axis('equal')

    return fig
