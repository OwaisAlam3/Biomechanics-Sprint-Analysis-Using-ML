import pandas as pd

# ----------------------------
# CONFIGURATION
# ----------------------------
trc_file = "C:\\Users\\T490\\OneDrive\\Desktop\\110_Internship_Tasks\\Sprint GSG Position Analysis\\results\\sports2d_output\\sprint_video_Sports2D\\sprint_video_Sports2D_m_person00.trc"

# Frames for key events (from your annotation)
frames = {
    "GET": 452,
    "SET": 479,
    "GO": 495,
    "Stride1_start": 495,
    "Stride1_end": 505,
    "Stride2_start": 510,
    "Stride2_end": 518
    # Stride3 not included; video ends
}

# ----------------------------
# LOAD TRC
# ----------------------------
# Skip first 4 rows (header info)
df = pd.read_csv(trc_file, sep='\t', skiprows=4)

# Columns mapping: joints -> Y column index
Y_cols = {
    "LShoulder": "Y21",
    "RShoulder": "Y19",
    "LHip": "Y11",
    "RHip": "Y7",
    "LKnee": "Y12",
    "RKnee": "Y8"
}

X_cols = {
    "LHip": "X11",
    "RHip": "X7"
}

# ----------------------------
# FUNCTIONS
# ----------------------------
def get_height(frame, joint):
    """Return Y (vertical) value for a joint at a specific frame."""
    row = df[df['Unnamed: 0'] == frame]
    if not row.empty:
        return row[Y_cols[joint]].values[0]
    else:
        return None

def get_stride_length(start_frame, end_frame, joint="LHip"):
    """Compute stride length along X for a joint."""
    row_start = df[df['Unnamed: 0'] == start_frame]
    row_end = df[df['Unnamed: 0'] == end_frame]
    if not row_start.empty and not row_end.empty:
        return abs(row_end[X_cols[joint]].values[0] - row_start[X_cols[joint]].values[0])
    else:
        return None

def posture_change(joint, from_frame, to_frame):
    """Vertical change from one frame to another."""
    h1 = get_height(from_frame, joint)
    h2 = get_height(to_frame, joint)
    if h1 is not None and h2 is not None:
        return h2 - h1
    else:
        return None

# ----------------------------
# CALCULATIONS
# ----------------------------
print("===== Heights at GET =====")
for j in ["LShoulder","RShoulder","LHip","RHip"]:
    print(f"{j}: {get_height(frames['GET'], j):.3f} m")

print("\n===== Heights at SET =====")
for j in ["LShoulder","RShoulder","LHip","RHip","LKnee","RKnee"]:
    print(f"{j}: {get_height(frames['SET'], j):.3f} m")

print("\n===== Stride Lengths =====")
for i, s in enumerate([("Stride1_start","Stride1_end"), ("Stride2_start","Stride2_end")], start=1):
    l = get_stride_length(frames[s[0]], frames[s[1]])
    print(f"Stride {i}: {l:.3f} m")

print("\n===== Posture Changes (vertical) from GO =====")
for joint in ["LShoulder","RShoulder","LHip","RHip","LKnee","RKnee"]:
    for stride_end in ["Stride1_end","Stride2_end"]:
        delta = posture_change(joint, frames["GO"], frames[stride_end])
        print(f"{joint}_GO_to_{stride_end}: {delta:.3f} m")
