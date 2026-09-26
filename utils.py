
import pandas as pd
import numpy as np

CHANNEL_NAMES = [
    "accelerometer_x",
    "accelerometer_y",
    "accelerometer_z",
    "gravity_x",
    "gravity_y",
    "gravity_z",
    "gyros_x",
    "gyros_y",
    "gyros_z",
    "lin_accel_x",
    "lin_accel_y",
    "lin_accel_z",
    "game_rot_vec_x",
    "game_rot_vec_y",
    "game_rot_vec_z",
    "magn_field_x",
    "magn_field_y",
    "magn_field_z"
]


"""
Function that splits the input into data and labels (movements)
"""
def input_generation(input_path, ablation, ABLATION_CHANNELS):

    X = []      # -> input signals data     
    y = []      # -> movements (labels)

    channel_names = CHANNEL_NAMES

    csv_files = sorted(input_path.glob("*.csv"))

    for file_path in csv_files:

        # labels
        movement = int(file_path.stem.split("-")[0])
        y.append(movement)

        # data
        df = pd.read_csv(file_path)
        x = df.to_numpy(dtype=np.float32).T
        
        X.append(x)

    y = np.array(y)


    # if ablation
    if ablation:
        channels_to_remove = ABLATION_CHANNELS[ablation]

        X = [np.delete(x, channels_to_remove, axis=0) for x in X]
        channel_names = [name for i, name in enumerate(channel_names) if i not in channels_to_remove]

    return X, y, channel_names