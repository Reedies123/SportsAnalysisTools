import csv
import math

def calculate_total_distance(csv_file):
    positions = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row['x'])
            y = float(row['y'])
            positions.append((x, y))

    total_distance = 0.0
    for i in range(1, len(positions)):
        x1, y1 = positions[i - 1]
        x2, y2 = positions[i]
        distance = math.hypot(x2 - x1, y2 - y1)
        total_distance += distance

    return total_distance

def calculate_time_in_regions(csv_file):
    """
    Splits the pitch into 3 equal regions along y:
    Region 1: -50 to -16.67
    Region 2: -16.67 to +16.67
    Region 3: +16.67 to +50
    Returns the time spent in each region (assuming 1 time unit per row).
    """
    region_bounds = [-50, -16.67, 16.67, 50]
    region_times = [0, 0, 0]

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            y = float(row['y'])
            if region_bounds[0] <= y < region_bounds[1]:
                region_times[0] += 1
            elif region_bounds[1] <= y < region_bounds[2]:
                region_times[1] += 1
            elif region_bounds[2] <= y <= region_bounds[3]:
                region_times[2] += 1

    return region_times

def calculate_sprint_time(csv_file):
    """
    Calculates the time spent sprinting (speed > 3 m/s).
    Assumes each row is 1 second apart.
    """
    positions = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row['x'])
            y = float(row['y'])
            positions.append((x, y))

    sprint_time = 0
    for i in range(1, len(positions)):
        x1, y1 = positions[i - 1]
        x2, y2 = positions[i]
        distance = math.hypot(x2 - x1, y2 - y1)
        speed = distance / 1  # seconds between samples
        if speed > 3:
            sprint_time += 1

    return sprint_time

def calculate_quick_turns(csv_file):
    """
    Counts the number of quick turns: a change in direction > 90 degrees following a sprint (>3 m/s).
    """
    positions = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row['x'])
            y = float(row['y'])
            positions.append((x, y))

    quick_turns = 0
    for i in range(2, len(positions)):
        # Calculate speed for previous segment
        x0, y0 = positions[i - 2]
        x1, y1 = positions[i - 1]
        x2, y2 = positions[i]
        dist_prev = math.hypot(x1 - x0, y1 - y0)
        speed_prev = dist_prev / 1  # seconds between samples

        # Only consider if previous segment was a sprint
        if speed_prev > 3:
            # Calculate direction vectors
            v1 = (x1 - x0, y1 - y0)
            v2 = (x2 - x1, y2 - y1)
            # Calculate angle between vectors
            dot = v1[0]*v2[0] + v1[1]*v2[1]
            mag1 = math.hypot(*v1)
            mag2 = math.hypot(*v2)
            if mag1 == 0 or mag2 == 0:
                continue
            cos_theta = dot / (mag1 * mag2)
            # Clamp to valid range to avoid math domain error
            cos_theta = max(-1.0, min(1.0, cos_theta))
            angle = math.degrees(math.acos(cos_theta))
            if angle > 90:
                quick_turns += 1

    return quick_turns

def generate_heatmap(csv_file, bins=(50, 30), output_path=None):
    """
    Generates and saves a heatmap of player positions on a football pitch.
    Pitch is centered at (0,0), 100m in y (-50 to +50), 60m in x (-30 to +30).
    """
    import matplotlib.pyplot as plt
    import numpy as np

    x_positions = []
    y_positions = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x_positions.append(float(row['x']))
            y_positions.append(float(row['y']))

    plt.figure(figsize=(8, 12))
    plt.hexbin(x_positions, y_positions, gridsize=bins, cmap='hot', extent=[-30, 30, -50, 50])
    plt.colorbar(label='Density')
    plt.title('Player Position Heatmap')
    plt.xlabel('X position (m)')
    plt.ylabel('Y position (m)')
    plt.xlim(-30, 30)
    plt.ylim(-50, 50)
    plt.gca().set_aspect('equal', adjustable='box')
    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def generate_vector_map(csv_file, output_path):
    """
    Generates and saves a vector map of player movement across the pitch.
    Line segments are color-coded by speed (red=slow, white=fast).
    Pitch background is green.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.colors as mcolors

    positions = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x = float(row['x'])
            y = float(row['y'])
            positions.append((x, y))

    # Calculate speeds for each segment
    speeds = []
    for i in range(1, len(positions)):
        x1, y1 = positions[i - 1]
        x2, y2 = positions[i]
        distance = math.hypot(x2 - x1, y2 - y1)
        speed = distance / 1  # seconds between samples
        speeds.append(speed)

    # Normalize speeds for color mapping
    speeds_np = np.array(speeds)
    min_speed = speeds_np.min() if len(speeds_np) > 0 else 0
    max_speed = speeds_np.max() if len(speeds_np) > 0 else 1
    norm = plt.Normalize(min_speed, max_speed)

    # Create custom colormap: red (slow) to white (fast)
    cmap = mcolors.LinearSegmentedColormap.from_list("speedmap", ["red", "white"])

    fig, ax = plt.subplots(figsize=(8, 12))
    # Draw green pitch background
    ax.set_facecolor('green')
    ax.set_xlim(-30, 30)
    ax.set_ylim(-50, 50)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Player Movement Vector Map')
    ax.set_xlabel('X position (m)')
    ax.set_ylabel('Y position (m)')

    # Draw movement lines
    for i in range(1, len(positions)):
        x1, y1 = positions[i - 1]
        x2, y2 = positions[i]
        speed = speeds[i - 1]
        color = cmap(norm(speed))
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=2)

    # Add colorbar for speed
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', label='Speed (m/s)')

    plt.savefig(output_path, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    csv_path = "/workspaces/SportsAnalysisTools/TestData/testdata.csv"
    total_distance = calculate_total_distance(csv_path)
    print(f"Total distance ran: {total_distance:.2f} metres")

    region_times = calculate_time_in_regions(csv_path)
    print("Time spent in each region:")

    for i, seconds in enumerate(region_times, 1):
        minutes = seconds // 60
        secs = seconds % 60
        print(f"Region {i}: {minutes} min {secs} sec")

    sprint_time = calculate_sprint_time(csv_path)
    sprint_minutes = sprint_time // 60
    sprint_seconds = sprint_time % 60
    print(f"Time spent sprinting (>3 m/s): {sprint_minutes} min {sprint_seconds} sec")

    quick_turns = calculate_quick_turns(csv_path)
    print(f"Total number of quick turns (>90° after sprint): {quick_turns}")

    # Save the heatmap as a PNG in the TestData folder
    heatmap_path = "/workspaces/SportsAnalysisTools/TestData/heatmap.png"
    generate_heatmap(csv_path, output_path=heatmap_path)
    print(f"Heatmap saved to {heatmap_path}")

    # Generate and save vector map
    vectormap_path = "/workspaces/SportsAnalysisTools/TestData/vectormap.png"
    generate_vector_map(csv_path, output_path=vectormap_path)
    print(f"Vector map saved to {vectormap_path}")