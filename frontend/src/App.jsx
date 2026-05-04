import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadFile = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);

    } catch (err) {
      console.error(err);
      alert("Error uploading file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", maxWidth: "700px", margin: "auto" }}>
      
      <h1 style={{ marginBottom: "20px" }}>Music AI 🎵</h1>

      {/* ================= STEP 2: UPLOAD BOX ================= */}
      <div
        style={{
          padding: "20px",
          border: "2px dashed #2EC4B6",
          borderRadius: "12px",
          textAlign: "center"
        }}
      >
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <br /><br />

        <button
          onClick={uploadFile}
          style={{
            padding: "10px 20px",
            background: "#E71D36",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer"
          }}
        >
          Analyze Song
        </button>
      </div>

      {/* LOADING */}
      {loading && <p style={{ marginTop: "20px" }}>Analyzing...</p>}

      {/* ================= STEP 1: RESULT UI ================= */}
      {result && (
        <div style={{ marginTop: "30px" }}>
          
          <h2 style={{ marginBottom: "10px" }}>🎵 Analysis Result</h2>

          {/* FILE */}
          <p style={{ opacity: 0.7 }}>{result.filename}</p>

          {/* CARDS */}
          <div style={{ display: "flex", gap: "20px", marginTop: "20px" }}>
            
            {/* TEMPO */}
            <div style={{
              padding: "20px",
              borderRadius: "12px",
              background: "#2EC4B6",
              color: "white",
              minWidth: "120px"
            }}>
              <p style={{ margin: 0, fontSize: "14px" }}>Tempo</p>
              <h2 style={{ margin: 0 }}>{result.tempo_bpm} BPM</h2>
            </div>

            {/* KEY */}
            <div style={{
              padding: "20px",
              borderRadius: "12px",
              background: "#FF9F1C",
              color: "white",
              minWidth: "120px"
            }}>
              <p style={{ margin: 0, fontSize: "14px" }}>Key</p>
              <h2 style={{ margin: 0 }}>{result.key}</h2>
            </div>

          </div>

          {/* CHORDS */}
          <div style={{ marginTop: "25px" }}>
            <p style={{ marginBottom: "10px", fontWeight: "bold" }}>
              Chord Progression
            </p>

            {/* INSTRUMENTS */}
            <div style={{ marginTop: "10px" }}>
              <p style={{ marginBottom: "10px", fontWeight: "bold" }}>
                Instruments
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
                {result?.instruments?.length ? (
                  result.instruments.map((instrument, index) => (
                    <span
                      key={index}
                      style={{
                        padding: "10px 14px",
                        background: "#FF9F1C",
                        color: "white",
                        borderRadius: "20px",
                        fontWeight: "bold"
                      }}
                    >
                      {instrument}
                    </span>
                  ))
                ) : (
                  <p>No instruments detected</p>
                )}
              </div>
            </div>

            <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
              {result?.chords?.length ? (
                result.chords.map((chord, index) => (
                  <span
                    key={index}
                    style={{
                      padding: "8px 14px",
                      background: "#2EC4B6",
                      color: "white",
                      borderRadius: "20px",
                      fontWeight: "bold"
                    }}
                  >
                    {chord}
                  </span>
                ))
              ) : (
                <p>No chords detected</p>
              )}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}

export default App;