import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>Music AI Analyzer</h1>

      <input
        type="file"
        accept=".mp3,.wav"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={uploadFile}>Upload Song</button>

      <br /><br />

      {result && (
        <div>
          <h3>Analysis Result</h3>
          <p><b>File:</b> {result.filename}</p>
          <p><b>Duration:</b> {result.duration_seconds} sec</p>
          <p><b>Sample Rate:</b> {result.sample_rate}</p>
          <p><b>Tempo:</b> {result.tempo_bpm} BPM</p>
          <p><b>Status:</b> {result.status}</p>
        </div>
      )}
    </div>
  );
}

export default App;