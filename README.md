# SportsAnalysisTools
Suite of tools for analysing sports science data, including tracking data and biomechanics.

## Features

The `src/trackervis.py` module provides the following analysis tools for football player tracking data:

- **Total Distance Calculation**: Computes the total distance covered by the player.
- **Time in Pitch Regions**: Splits the pitch into three regions and calculates time spent in each.
- **Sprint Time**: Calculates total time spent sprinting (speed > 3 m/s).
- **Quick Turns Detection**: Counts the number of quick turns (>90° change in direction after a sprint).
- **Heatmap Generation**: Creates a heatmap of player positions and saves it as a PNG.
- **Vector Map Visualization**: Generates a vector map of player movement, color-coded by speed (red=slow, white=fast), with a green pitch background, and saves it as a PNG.

## Usage

Run `src/trackervis.py` to process a CSV file containing player tracking data and generate analysis outputs in the `TestData` folder.
