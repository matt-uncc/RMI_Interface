import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Load your CSV points
csv_file = r'C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\csv\one_line_drawing.csv'  # change to your file path

x_points = []
y_points = []

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        x_points.append(float(row[0]))
        y_points.append(float(row[1]))

fig, ax = plt.subplots()
scatter = ax.scatter([], [])

ax.set_xlim(min(x_points) - 1, max(x_points) + 1)
ax.set_ylim(min(y_points) - 1, max(y_points) + 1)
plt.gca().invert_yaxis()  # invert if coordinates are image-like

def update(frame):
    if frame > 0:
        scatter.set_offsets(list(zip(x_points[:frame], y_points[:frame])))
    return scatter,

ani = animation.FuncAnimation(fig, update, frames=len(x_points)+1,
                              interval=100, blit=True, repeat=False)

plt.show()
