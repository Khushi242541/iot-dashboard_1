#from backend.server.mongo import *
from tkinter import *
from tkinter.ttk import Treeview
from datetime import datetime
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from frontend.graph.graphnew import create_production_data 
from backend.server.mongo import fetch_recipe_data, fetch_continuous_data, fetch_production_data, fetch_graphdata, fetch_pie_chart 
from frontend.graph.pie_chart import draw_pie_chart

# Root setup
root = Tk()
root.title("Dashboard UI")
root.geometry("1200x700")
root.configure(bg="#fdf6f6")

# GUI values (declaring)    
p1v1 =tk.StringVar()
p1v2 =tk.StringVar()
p2v1 =tk.StringVar()
p2v2 =tk.StringVar()

# Fetch and assign MongoDB values
mongo_values = fetch_production_data()
if mongo_values:
    p1v1.set(mongo_values.get("p1v1", "N/A"))
    p1v2.set(mongo_values.get("p1v2", "N/A"))
    p2v1.set(mongo_values.get("p2v1", "N/A"))
    p2v2.set(mongo_values.get("p2v2", "N/A"))
else:
    p1v1.set("N/A")
    p1v2.set("N/A")
    p2v1.set("N/A")
    p2v2.set("N/A")

# ---------------- DATETIME DISPLAY ----------------
def update_time():
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    time_label.configure(text=now)
    root.after(1000, update_time)
time_label = Label(root, text="", font=("Arial", 14))
time_label.pack(pady=10, side="top")
update_time()

# Top bar
Frame(root, bg="#d7d8d8", height=40).pack(fill=X)
Frame(root, bg="#4a2f78", height=2).pack(fill=X)

# Main layout frame
main_frame = Frame(root, bg="#fdf6f6")
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Left and right sections---- the table and status is on top of this field-----
left_frame = Frame(main_frame, bg="#e4f0f2", width=1050)
left_frame.pack(side=LEFT, fill=Y, expand=False)
left_frame.pack_propagate(False)

right_frame = Frame(main_frame, bg="#a5badf")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True) 


#Recipe Table (now placed at top of left_frame) 
# # # Define column headings (table)
recipe_tree = Treeview(left_frame, columns=("col1", "col2", "col3"), show='headings', height=5)
recipe_tree.heading("col1", text="Previous recipe")
recipe_tree.heading("col2", text="Current recipe")
recipe_tree.heading("col3", text="Next recipe")
recipe_tree.column("col1", anchor='center', width=50)
recipe_tree.column("col2", anchor='center', width=50)
recipe_tree.column("col3", anchor='center', width=50)
recipe_tree.pack(fill=X, padx=5, anchor='center', pady=(2, 5))

recipes = fetch_recipe_data()
print("Recipe List:", recipes)  # DEBUG: see what's coming

if recipes:
    for r in recipes:
        recipe_tree.insert("", "end", values=(r["previous"], r["current"], r["next"]))
else:
    recipe_tree.insert("", "end", values=("N/A", "N/A", "N/A"))

# Box configuration
production_blocks = [
    [("Production1-a", p1v1, "#ffcc29"), ("Production1-b", p1v2, "#00ff00")],
    [("Production2-b", p2v1, "#ffcc29"), ("Production2-b", p2v2, "#00ff00")]
]
color_row = Frame(left_frame, bg="#dcdcdc", padx=20, pady=10)
color_row.pack(fill=X, pady=10)

for pair in production_blocks:
    pair_frame = Frame(color_row, bg="#dcdcdc")
    pair_frame.pack(side=LEFT, padx=20)

    for label_text, var, color in pair:
        box = Frame(pair_frame, bg=color, width=180, height=80)
        box.pack(side=LEFT, padx=25, pady=20)
        box.pack_propagate(False)  # This line keeps size fixed!

        Label(box, text=label_text, bg=color, font=("Arial", 10, "bold")).pack()
        Label(box, textvariable=var, bg=color, font=("Arial", 12)).pack()
data2=fetch_production_data()
print("Data", data2)

# ######
# #Horizontal stack (for the purpose of graphs)
# legend_frame = Frame(left_frame, bg="#dcdcdc")
# legend_frame.pack(fill=X, pady=(10, 0))
# legend = Frame(legend_frame, bg='white', padx=5, pady=5)

# create_production_data(legend_frame)
# data3=fetch_graphdata()
# print("Data3", data3)

# for col, txt in colors: 
###############################################################################
#---------------- RIGHT PANEL ----------------
# Buttons
Button(right_frame, text="\U0001F5C2 ITEM QUEUE", bg="#3c5cff", fg="white", font=("Arial", 10, "bold"), relief="raised", padx=15, pady=15).pack(padx=10, pady=10, fill=X)
Button(right_frame, text="\U0001F464 OPERATOR CHANGE", bg="#839dff", fg="white", font=("Arial", 10), relief="raised", padx=15, pady=15).pack(padx=10, pady=10, fill=X)

# Notes section -----------------------------   NOTES  -----------------------------------------------
Label(right_frame, text="Notes", bg="#5f6670", fg="white", anchor=W).pack(fill=X, padx=10, pady=(10, 0))
# Frame(right_frame, bg="light grey", width=80, height=80).pack(fill=X,padx=10)
LabelFrame(right_frame,text="Static values here right now", bg="light grey", width=180, height=80).pack(fill=X,padx=10)

#Treeview Scrollable Listbox
Label(right_frame, text="Item List", bg="#3c5cff", fg="white", font=("Arial", 10, "bold")).pack(fill=X,padx=20, pady=(20, 0))
tree_frame = Frame(right_frame, bg="#f0f4f7")
tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=5) #the box wher e scrollbar is fitted

#Inner holder frame to pack Treeview and Scrollbar side by side
tree_holder = Frame(tree_frame, bg="#f0f4f7")
tree_holder.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(tree_holder)
scrollbar.pack(side=RIGHT, fill=Y)

tree = Treeview(tree_holder, columns=("item", "qty"), show="headings", yscrollcommand=scrollbar.set)
tree.heading("item", text="BOM Item")
tree.heading("qty", text="Qty")
tree.column("item", anchor=W, width=20)
tree.column("qty", anchor=E, width=20)

tree.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.configure(command=tree.yview)

# Fetch from Mongo
data_list = fetch_continuous_data()

# Insert into Treeview
for item in data_list:
    code = item.get("code", "N/A")       # Use the field names as per your MongoDB schema
    value = item.get("value", "N/A")
    tree.insert("", END, values=(code, value))

# Insert sample data
# for i in range(1, 20):
#     tree.insert("", END, values=(f"WFCVGHCHGV7{i}/0.652", f"86.9600{i}"))
# PIE CHART EMBEDDED INSIDE LEFT_FRAME

# ---------------- GRAPHS: PIE CHART + HORIZONTAL STACKED BAR SIDE-BY-SIDE ----------------
charts_frame = Frame(left_frame, bg="#e3beeb")
charts_frame.pack(fill=X, pady=(10, 20))

# PIE CHART on the LEFT
pie_frame = Frame(charts_frame, bg="#ffffff")
pie_frame.pack(side=LEFT, padx=10)

fig = draw_pie_chart()
if fig:
    canvas = FigureCanvasTkAgg(fig, master=pie_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
else:
    Label(pie_frame, text="No pie data available", bg="#fdf0f0", fg="red", font=("Arial", 10)).pack()

# STACKED BAR GRAPH on the RIGHT
bar_frame = Frame(charts_frame, bg="#b51ec0")
bar_frame.pack(side=LEFT, padx=10)

create_production_data(bar_frame)

data3 = fetch_graphdata()
print("Data3", data3)
hour_selection_frame = Frame(left_frame, bg="#681788")
hour_selection_frame.pack(pady=(5, 5))

Label(hour_selection_frame, text="Enter Hour (0-23):", bg="#d88383", font=("Arial", 10)).pack(side=LEFT)
hour_var = StringVar()
Entry(hour_selection_frame, textvariable=hour_var, width=5).pack(side=LEFT, padx=(5, 10))

#  Button(hour_selection_frame, text="Update Chart", command=lambda: update_pie_chart_by_hour(hour_var.get())).pack(side=LEFT)


##Pie chart graph 
# pie_chart=fetch_pie_chart()

# Mainloop
root.mainloop()
 