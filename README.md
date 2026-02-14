# Sprint Start Biomechanics Analysis

A Python-based tool for analyzing athlete posture and movement during sprint starts using 2D motion capture data from Sports2D.

## Overview

This project analyzes key biomechanical parameters of sprint starts, including body positioning during the GET-SET-GO sequence, stride lengths, and posture changes throughout the acceleration phase.

## Features

- **Phase Analysis**: Extracts joint positions during GET, SET, and GO phases
- **Height Measurements**: Calculates vertical positions of key joints (shoulders, hips, knees, ankles)
- **Stride Length**: Computes horizontal displacement for each stride
- **Posture Changes**: Tracks vertical movement of joints from GO through stride phases
- **Pixel-to-Meter Conversion**: Converts pixel coordinates to real-world measurements using athlete height calibration

## Requirements

Install dependencies:
```bash
pip install pandas numpy
```

Full requirements available in `requirements.txt` (includes additional packages for extended functionality).

## Usage

### Script 1: Meter-based Analysis (`script_analysis_2d.py`)

For TRC files with direct meter coordinates:

```python
# Configure your TRC file path
trc_file = "path/to/your/sprint_video_Sports2D_m_person00.trc"

# Define frame numbers for key events
frames = {
    "GET": 452,
    "SET": 479,
    "GO": 495,
    "Stride1_start": 495,
    "Stride1_end": 505,
    # ...
}

python script_analysis_2d.py
```

### Script 2: Pixel-based Analysis (`scrip_v2.py`)

For TRC files with pixel coordinates (requires calibration):

```python
# Configure parameters
TRC_PATH = "path/to/your/sprint_video_Sports2D_px_person00.trc"
FRAME_GROUND = 101          # Frame with feet on ground
FRAME_UPRIGHT = 44          # Frame with athlete fully upright
ATHLETE_HEIGHT_M = 1.88     # Athlete height in meters

python scrip_v2.py
```

## Sprint Start Phases

- **GET (Frame 452)**: "On the blocks" position - hands on ground, rear knee down
- **SET (Frame 479)**: Ready position - knees off ground, hips raised
- **GO (Frame 495)**: Push-off begins - hands leave ground, body rises

## Output

Both scripts output:
- Joint heights at GET and SET positions
- Stride lengths for each stride
- Vertical posture changes from GO through stride phases

Example output:
```
===== Heights at GET =====
LShoulder: 0.845 m
RShoulder: 0.842 m
...

===== Stride Lengths =====
Stride 1: 1.234 m
Stride 2: 1.567 m
```

## File Structure

- `script_analysis_2d.py` - Main analysis script (meter coordinates)
- `scrip_v2.py` - Analysis with pixel-to-meter conversion
- `state_identification_method.txt` - Sprint phase descriptions
- `frames_selection.txt` - Frame number reference
- `requirements.txt` - Python dependencies

## Input Data Format

Requires TRC (Track Row Column) files from Sports2D motion capture, containing joint coordinates for each frame.

## Notes

- Adjust frame numbers in the configuration section based on your video
- For pixel-based analysis, ensure accurate athlete height and calibration frames
- TRC files should contain standard joint markers (shoulders, hips, knees, ankles, etc.)