import os
import librosa
import numpy as np
import pandas as pd

DATASET_PATH = "your_audio_folder"
data = []

for label in os.listdir(DATASET_PATH):
    class_path = os.path.join(DATASET_PATH, label)

    for file in os.listdir(class_path):
        if file.endswith(".wav"):
            path = os.path.join(class_path, file)

            y, sr = librosa.load(path, sr=22050)

            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc, axis=1)

            data.append(list(mfcc_mean) + [label])

df = pd.DataFrame(data)
df.to_csv("features.csv", index=False)

print("Dataset created!")