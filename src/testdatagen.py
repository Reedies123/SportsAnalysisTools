import csv
import random
import os
import math
 
def generate_tracking_data(writer, identifier, num_rows=2700, attraction_point=(0, 0)):
    """
    Generates and writes simulated player tracking data to a CSV writer,
    mimicking a midfielder's movement.

    - Movement has inertia to create smoother paths.
    - Player tends to stay towards the center of the pitch.
    - Mix of jogging and occasional sprints.

    Args:
        writer (csv.writer): The CSV writer object to write data to.
        identifier (any): The identifier for the entity being tracked.
        num_rows (int, optional): The number of data rows to generate. Defaults to 2700.
        attraction_point (tuple, optional): The (x, y) point the player is attracted to. Defaults to (0, 0).
    """
    x_min, x_max = -30, 30
    y_min, y_max = -50, 50
 
    x, y = 0, 0
    vx, vy = 0, 0  # Velocity components

    # Simulation parameters
    max_speed = 7.0  # m/s, realistic top speed
    sprint_chance = 0.02  # Chance to start sprinting each second
    sprint_duration_counter = 0  # Ticks left in current sprint
    # How strongly player is pulled to center. The force is weak in the middle
    # and grows with the square of the distance from the center.
    max_attraction_force = 0.2  # The max acceleration applied at the boundary.

    attraction_x, attraction_y = attraction_point
 
    for t in range(1, num_rows + 1):
        # --- Acceleration ---
        # Base random acceleration for natural movement
        ax = random.uniform(-0.15, 0.15)
        ay = random.uniform(-0.15, 0.15)

        # Attraction to a specific point (force proportional to distance squared from point)
        dx = x - attraction_x
        dy = y - attraction_y
        ax -= (dx / x_max) * abs(dx / x_max) * max_attraction_force
        ay -= (dy / y_max) * abs(dy / y_max) * max_attraction_force

        # --- Sprinting Logic ---
        if sprint_duration_counter > 0:
            # In a sprint, accelerate more in the current direction
            sprint_boost = 1.0
            if math.hypot(vx, vy) > 0.1:  # only boost if already moving
                ax += (vx / math.hypot(vx, vy)) * sprint_boost
                ay += (vy / math.hypot(vx, vy)) * sprint_boost
            sprint_duration_counter -= 1
        elif random.random() < sprint_chance:
            # Start a sprint for a short duration
            sprint_duration_counter = random.randint(3, 7)

        # --- Velocity and Speed Update ---
        # Update velocity with acceleration
        vx += ax
        vy += ay

        # Apply drag/friction to slow down over time
        vx *= 0.90
        vy *= 0.90

        # Cap speed to max_speed
        speed = math.hypot(vx, vy)
        if speed > max_speed:
            vx = (vx / speed) * max_speed
            vy = (vy / speed) * max_speed

        # --- Position Update ---
        x += vx
        y += vy

        # Boundary collision
        if not (x_min < x < x_max):
            x = max(x_min, min(x_max, x))
            vx *= -0.5  # Bounce off with reduced velocity
        if not (y_min < y < y_max):
            y = max(y_min, min(y_max, y))
            vy *= -0.5  # Bounce off with reduced velocity

        writer.writerow([identifier, t, round(x, 2), round(y, 2)])
 
def generate_player_metadata(player_setup, output_path):
    """
    Generates a CSV file with randomized, realistic player metadata.

    Args:
        player_setup (list): A list of tuples, where each tuple contains
                             the player identifier.
        output_path (str): The path to save the output CSV file.
    """
    # Generate unique shirt numbers from 1-99
    shirt_numbers = random.sample(range(1, 100), len(player_setup))

    with open(output_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["identifier", "shirt_number", "age", "height_cm", "weight_kg"])

        for i, (identifier, _) in enumerate(player_setup):
            shirt_number = shirt_numbers[i]
            age = random.randint(18, 38)
            height_cm = random.randint(170, 200)
            weight_kg = random.randint(65, 95)
            csv_writer.writerow([identifier, shirt_number, age, height_cm, weight_kg])

if __name__ == "__main__":
    # --- Setup Paths ---
    output_dir = os.path.join(os.path.dirname(__file__), "..", "TestData")
    os.makedirs(output_dir, exist_ok=True)
    tracking_filepath = os.path.join(output_dir, "trackingdata.csv")
 
    # --- Define Player Setup ---
    # Players are defined by an identifier and an "attraction point" on the pitch,
    # simulating their average position in a 4-3-3 formation.
    player_setup = [
        ("GK",  (0, -45)),   # Goalkeeper
        ("RB",  (20, -30)),  # Right Back
        ("RCB", (10, -35)),  # Right Center Back
        ("LCB", (-10, -35)), # Left Center Back
        ("LB",  (-20, -30)), # Left Back
        ("RCM", (15, 0)),    # Right Central Midfielder
        ("CM",  (0, -10)),   # Central Midfielder
        ("LCM", (-15, 0)),   # Left Central Midfielder
        ("RW",  (25, 20)),   # Right Winger
        ("ST",  (0, 30)),    # Striker
        ("LW",  (-25, 20)),  # Left Winger
    ]
 
    # --- Generate Tracking Data ---
    with open(tracking_filepath, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["identifier", "time", "x", "y"])
        total_rows = 0
        for identifier, attraction_point in player_setup:
            num_rows = 2700  # ~45 minutes at 1Hz
            generate_tracking_data(csv_writer, identifier, num_rows, attraction_point)
            total_rows += num_rows
 
    print(f"Generated a total of {total_rows} rows for {len(player_setup)} players at {tracking_filepath}")

    # --- Generate Player Metadata ---
    metadata_filepath = os.path.join(output_dir, "player_data.csv")
    generate_player_metadata(player_setup, metadata_filepath)
    print(f"Generated player metadata for {len(player_setup)} players at {metadata_filepath}")