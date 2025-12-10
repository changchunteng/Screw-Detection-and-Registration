# Screw Detection and Registration System

This project performs point-set registration between prior screw locations and detected screw positions, identifying missing, extra, and correctly matched screws.

## Usage


### 1. Prepare your prior screw information as `PriorData.txt`

Format: Space-separated values with coordinates in columns 2-3 (zero-based indexing).

### 2. Prepare your detection results as `DetectionData.txt`

Format: Space-separated values with coordinates in columns 2-3 (zero-based indexing).

### 3. Run the registration script

Execute the main script:

python Screw-Detection-and-Registration.py


1. **Registration**: Uses Coherent Point Drift (CPD) algorithm to align the detected points with prior points
2. **Matching**: Performs Hungarian algorithm-based optimal matching between registered points
3. **Classification**: Identifies three types of screws:
   - **Correctly matched screws** (connected by dashed lines)
   - **Extra screws** (red points) - detected but not in prior data
   - **Missing screws** (purple points) - in prior data but not detected

## Output

The script generates a visualization showing:
- Prior screw positions (blue)
- Detection results (green)
- Registration results (light blue)
- Dashed lines connecting matched pairs
- Red points for extra screws
- Purple points for missing screws
