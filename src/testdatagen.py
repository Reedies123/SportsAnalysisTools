import csv
import random
import os

filename = "testdata.csv"
output_dir = os.path.join(os.path.dirname(__file__), "..", "TestData")
os.makedirs(output_dir, exist_ok=True)
filepath = os.path.join(output_dir, filename)

num_rows = 2700
x_min, x_max = -30, 30
y_min, y_max = -50, 50

x, y = 0, 0

with open(filepath, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time", "x", "y"])
    for t in range(1, num_rows + 1):
        dx = random.uniform(-3, 3)
        dy = random.uniform(-3, 3)
        x = max(x_min, min(x_max, x + dx))
        y = max(y_min, min(y_max, y + dy))
        writer.writerow([t, round(x, 2), round(y, 2)])