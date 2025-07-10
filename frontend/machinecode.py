import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
from datetime import datetime

# Sample simulated device data
sample_data = [
    {"ts": 1737182343 + i * 300, "Act_Line_Speed": 0 if i % 3 == 0 else random.uniform(40, 60)}
    for i in range(12)
]

# Convert timestamp to readable time
def ts_to_time(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M")

# Classify segments and assign colors
segments = []
for i in range(len(sample_data) - 1):
    start = sample_data[i]
    end = sample_data[i + 1]
    segments=(sample_data)
    segments.append
    
    duration = (end["ts"] - start["ts"]) / 60  # in minutes
    if start["Act_Line_Speed"] == 0:
        segments.append({
            "start_ts": start["ts"],
            "end_ts": end["ts"],
            "duration": duration,
            "type": "downtime",
            "reason": None
        })
    else:
        segments.append({
            "start_ts": start["ts"],
            "end_ts": end["ts"],
            "duration": duration,
            "type": "runtime"
        })