# 🎵 Music AI — Audio Analysis & Feature Extraction Pipeline

An end-to-end system for analyzing music/audio files using signal processing and machine learning techniques.  
This project focuses on extracting meaningful audio features and building structured pipelines for downstream ML tasks.

---

## 🚀 Features

- 🎧 Upload audio files via a React frontend
- ⚡ FastAPI backend for real-time audio processing
- 🎼 Extracts:
  - Tempo (BPM)
  - Musical Key
  - Chord Progression (basic estimation)
- 🧩 Modular pipeline design for future ML integration

---

## 🧠 Project Overview

This project is designed as a **progressive machine learning pipeline**, moving from raw audio signals → feature extraction → model training → evaluation.

### Current Capabilities

- Audio loading and preprocessing
- Feature extraction using:
  - MFCC (Mel-Frequency Cepstral Coefficients)
  - Spectral features
  - Temporal features
- Basic rule-based musical analysis (tempo, key, chords)
- API-based inference system with UI integration

---

## 🧠 Deep Learning Extension (research direction and work in progress)

This project is being extended towards deep learning-based audio understanding, with a focus on learning representations directly from raw or transformed audio signals.

---

### 🎼 Input Representation Strategy

Instead of directly feeding raw waveforms, the system converts audio into structured representations:

- **Mel Spectrograms**
- **Log-Mel Spectrograms**
- **MFCC feature maps**

These representations transform temporal audio signals into 2D time-frequency domains, making them suitable for convolutional learning.

---

### 🏗️ Planned Model Architectures

#### 1. CNN-based Spectrogram Models

- Treat spectrograms as images
- Apply 2D Convolutional Neural Networks
- Capture:
  - Local frequency patterns
  - Temporal transitions
- Tasks:
  - Instrument classification
  - Genre detection
  - Audio tagging

---

#### 2. Temporal Modeling (CNN + RNN / LSTM)

To capture long-term dependencies in music:

- CNN for feature extraction
- RNN / LSTM layers for sequence modeling
- Enables:
  - Chord progression learning
  - Temporal pattern recognition

---

#### 3. Attention-Based Models (Exploratory)

- Self-attention mechanisms to identify important time-frequency regions
- Potential use in:
  - Complex chord recognition
  - Polyphonic audio understanding

---

### 📊 Dataset & Training Strategy

- Initial experiments based on structured datasets such as IRMAS
- Audio segmentation into fixed-length windows
- Data normalization and augmentation:
  - Time stretching
  - Pitch shifting
  - Noise injection

---

### ⚙️ Training Pipeline

- Feature extraction → spectrogram generation
- Dataset creation with labels
- Batch training using GPU acceleration
- Loss functions:
  - Cross-entropy (classification tasks)
- Evaluation:
  - Accuracy
  - Precision / Recall
  - Confusion matrix analysis

---

### 🔍 Model Analysis & Optimization

- Feature importance analysis
- Sensitivity to noise and audio quality
- Hyperparameter tuning:
  - Learning rate
  - Batch size
  - Network depth
- Regularization:
  - Dropout
  - Batch normalization

---

### 🔄 Current Status

- Classical ML models implemented as baselines
- Dataset structuring pipeline in progress
- CNN-based models under development
- Integration into API pipeline planned

---

### 🎯 Research Goals

- Improve generalization across diverse audio samples
- Build robust instrument classification system
- Enhance chord detection using learned representations
- Bridge signal processing and deep learning approaches

---

