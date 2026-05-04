from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import librosa
import numpy as np

# Create FastAPI app
app = FastAPI()

# Allow frontend to talk with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 12 musical notes
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']


# ---------------------------------------------------
# KEY DETECTION
# ---------------------------------------------------
def detect_key(chroma_vector):
    # Major and Minor scale patterns
    major_template = np.array([1,0,1,0,1,1,0,1,0,1,0,1])
    minor_template = np.array([1,0,1,1,0,1,0,1,1,0,1,0])

    best_score = -1
    best_key = "Unknown"

    # Try all 12 notes as root
    for i in range(12):
        major_score = np.dot(np.roll(major_template, i), chroma_vector)
        minor_score = np.dot(np.roll(minor_template, i), chroma_vector)

        if major_score > best_score:
            best_score = major_score
            best_key = NOTE_NAMES[i] + " Major"

        if minor_score > best_score:
            best_score = minor_score
            best_key = NOTE_NAMES[i] + " Minor"

    return best_key


# ---------------------------------------------------
# CHORD DETECTION
# ---------------------------------------------------
def detect_chord(chroma_vector):
    best_score = -1
    best_chord = "Unknown"

    for i in range(12):

        # Major chord = root + major third + fifth
        major_template = np.zeros(12)
        major_template[i] = 1
        major_template[(i + 4) % 12] = 1
        major_template[(i + 7) % 12] = 1

        # Minor chord = root + minor third + fifth
        minor_template = np.zeros(12)
        minor_template[i] = 1
        minor_template[(i + 3) % 12] = 1
        minor_template[(i + 7) % 12] = 1

        major_score = np.dot(major_template, chroma_vector)
        minor_score = np.dot(minor_template, chroma_vector)

        if major_score > best_score:
            best_score = major_score
            best_chord = NOTE_NAMES[i]

        if minor_score > best_score:
            best_score = minor_score
            best_chord = NOTE_NAMES[i] + "m"

    return best_chord


# ---------------------------------------------------
# REMOVE REPEATED CHORDS
# Example: C C C G G Am -> C G Am
# ---------------------------------------------------
def compress_chords(chord_list):
    final = []

    for chord in chord_list:
        if len(final) == 0 or chord != final[-1]:
            final.append(chord)

    return final


# Home route
@app.get("/")
def home():
    return {"message": "Backend running"}


def extract_features(y, sr):
    # MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)

    # Spectral features
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    zero_crossing = np.mean(librosa.feature.zero_crossing_rate(y))

    # Temporal features
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo_value = float(np.array(tempo).flatten()[0])

    return {
        "mfcc": mfcc_mean.tolist(),
        "spectral_centroid": float(spectral_centroid),
        "spectral_rolloff": float(spectral_rolloff),
        "zero_crossing_rate": float(zero_crossing),
        "tempo": tempo_value   # ✅ FIXED
}


# ---------------------------------------------------
# MAIN UPLOAD API
# ---------------------------------------------------
@app.post("/upload")
async def upload_song(file: UploadFile = File(...)):

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # Load song as mono audio
    y, sr = librosa.load(file_path, mono=True)
    features = extract_features(y, sr)

    # 🎯 SEGMENTATION (take 3 sec chunk)
    segment_length = 3  # seconds

    if len(y) > segment_length * sr:
        y = y[:segment_length * sr]

    # Song duration
    duration = librosa.get_duration(y=y, sr=sr)

    # Tempo detection
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo_value = float(np.asarray(tempo).reshape(-1)[0])

    # Full song chroma for key detection
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    detected_key = detect_key(chroma_mean)

    # ---------------------------------------------
    # CHORD PROGRESSION DETECTION
    # ---------------------------------------------
    chord_sequence = []

    # Split song into 5-second windows
    step = sr * 5

    for start in range(0, len(y), step):

        segment = y[start:start + step]

        # Ignore tiny leftover segments
        if len(segment) < sr:
            continue

        # Chroma of this segment
        seg_chroma = librosa.feature.chroma_stft(y=segment, sr=sr)
        seg_mean = seg_chroma.mean(axis=1)

        # Detect chord
        chord = detect_chord(seg_mean)

        chord_sequence.append(chord)

    # Remove repeats
    final_chords = compress_chords(chord_sequence)

    # TEMP instrument detection (rule-based placeholder)
    def detect_instruments(y, sr):
        """
        Placeholder function for instrument detection.
        Currently returns a static list.
        Can be replaced with ML model later.
        """
        return ["Guitar", "Drums"]
    # call function
    instruments = detect_instruments(y, sr)

    return {
        "filename": file.filename,
        "duration_seconds": round(float(duration), 2),
        "tempo_bpm": round(tempo_value, 2),
        "key": detected_key,
        "chords": final_chords,
        "progression": " → ".join(final_chords),
        "instruments": instruments,
        "features": features,
        "status": "analyzed"
    }

