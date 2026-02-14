import pandas as pd
import numpy as np

TRC_PATH = "C:\\Users\\T490\\OneDrive\\Desktop\\110_Internship_Tasks\\Sprint GSG Position Analysis\\results\\sports2d_output\\sprint_video_Sports2D\\sprint_video_Sports2D_px_person00.trc"
FRAME_GROUND = 101         # feet touching ground
FRAME_UPRIGHT = 44         # fully upright
ATHLETE_HEIGHT_M = 1.88    # 6 ft 2 in

FRAME_GET = 90             # example
FRAME_SET = 95
STRIDE1_END = 110
STRIDE2_END = 125


df = pd.read_csv(
    TRC_PATH,
    sep="\t",
    skiprows=4
)

# Fix common TRC issues
df.columns = df.columns.str.strip()
df = df.rename(columns={df.columns[0]: "Frame#"})

# Ensure Frame# is numeric
df["Frame#"] = pd.to_numeric(df["Frame#"], errors="coerce")


JOINT_INDEX = {
    "Hip": 1,

    "RHip": 2,
    "RKnee": 3,
    "RAnkle": 4,
    "RBigToe": 5,
    "RSmallToe": 6,
    "RHeel": 7,

    "LHip": 8,
    "LKnee": 9,
    "LAnkle": 10,
    "LBigToe": 11,
    "LSmallToe": 12,
    "LHeel": 13,

    "Neck": 14,
    "Head": 15,
    "Nose": 16,

    "RShoulder": 17,
    "RElbow": 18,
    "RWrist": 19,

    "LShoulder": 20,
    "LElbow": 21,
    "LWrist": 22,
}


def joint_xy(joint, frame):
    idx = JOINT_INDEX[joint]
    row = df[df["Frame#"] == frame]

    if row.empty:
        raise ValueError(f"Frame {frame} not found")

    x = row[f"X{idx}"].values[0]
    y = row[f"Y{idx}"].values[0]

    return x, y


def joint_y(joint, frame):
    return joint_xy(joint, frame)[1]


def height_px(joint, frame):
    return ground_y - joint_y(joint, frame)


def stride_length_px(joint, f1, f2):
    x1, _ = joint_xy(joint, f1)
    x2, _ = joint_xy(joint, f2)
    return abs(x2 - x1)


ground_y = max(
    joint_y("LHeel", FRAME_GROUND),
    joint_y("RHeel", FRAME_GROUND),
)

print(f"Estimated ground level (px): {ground_y:.2f}")


head_y = joint_y("Head", FRAME_UPRIGHT)
upright_height_px = ground_y - head_y

PIXEL_TO_METER = ATHLETE_HEIGHT_M / upright_height_px

print(f"Pixel-to-meter scale: {PIXEL_TO_METER:.6f} m/px")


JOINTS_HEIGHT = [
    "LShoulder", "RShoulder",
    "LHip", "RHip",
    "LKnee", "RKnee",
    "LAnkle", "RAnkle"
]

print("\n===== Heights at GET =====")
for j in JOINTS_HEIGHT:
    h = height_px(j, FRAME_GET) * PIXEL_TO_METER
    print(f"{j}: {h:.3f} m")

print("\n===== Heights at SET =====")
for j in JOINTS_HEIGHT:
    h = height_px(j, FRAME_SET) * PIXEL_TO_METER
    print(f"{j}: {h:.3f} m")


stride1 = stride_length_px("Hip", FRAME_GROUND, STRIDE1_END) * PIXEL_TO_METER
stride2 = stride_length_px("Hip", STRIDE1_END, STRIDE2_END) * PIXEL_TO_METER

print("\n===== Stride Lengths =====")
print(f"Stride 1: {stride1:.3f} m")
print(f"Stride 2: {stride2:.3f} m")


print("\n===== Posture Changes (vertical) from GO =====")
for j in ["LShoulder", "RShoulder", "LHip", "RHip", "LKnee", "RKnee"]:
    delta1 = (
        height_px(j, STRIDE1_END) - height_px(j, FRAME_GET)
    ) * PIXEL_TO_METER

    delta2 = (
        height_px(j, STRIDE2_END) - height_px(j, FRAME_GET)
    ) * PIXEL_TO_METER

    print(f"{j}_GO_to_Stride1_end: {delta1:.3f} m")
    print(f"{j}_GO_to_Stride2_end: {delta2:.3f} m")
