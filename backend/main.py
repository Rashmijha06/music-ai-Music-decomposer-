from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import librosa
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.post("/upload")
async def upload_song(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    y, sr = librosa.load(file_path, mono=True)

    duration = librosa.get_duration(y=y, sr=sr)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    tempo_value = float(np.asarray(tempo).reshape(-1)[0])

    return {
        "filename": file.filename,
        "duration_seconds": round(float(duration), 2),
        "sample_rate": int(sr),
        "tempo_bpm": round(tempo_value, 2),
        "status": "analyzed"
    }