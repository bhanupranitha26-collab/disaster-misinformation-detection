import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import {
  MapContainer,
  TileLayer,
  Circle
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const API = "http://127.0.0.1:8001";

function App() {
  const [view, setView] = useState("authority");
  const [theme, setTheme] = useState("dark");
  const [posts, setPosts] = useState([]);
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetchPosts();
    const interval = setInterval(fetchPosts, 4000);
    return () => clearInterval(interval);
  }, []);

  const fetchPosts = async () => {
    const res = await axios.get(`${API}/recent-posts`);
    setPosts(res.data);
  };

  const analyzeText = async () => {
    const res = await axios.post(`${API}/analyze-text`, { text });
    setResult(res.data);
    fetchPosts();
  };

  const approve = async (id) => {
    await axios.post(`${API}/approve/${id}`, { reviewer: "Admin" });
    fetchPosts();
  };

  const reject = async (id) => {
    await axios.post(`${API}/reject/${id}`, { reviewer: "Admin" });
    fetchPosts();
  };

  const fake = posts.filter(p => p.status.includes("Fake")).length;
  const review = posts.filter(p => p.status.includes("Review")).length;
  const verified = posts.filter(p => p.status.includes("Verified")).length;
  const avgPanic =
    posts.length > 0
      ? Math.round(posts.reduce((a, b) => a + b.panic_index, 0) / posts.length)
      : 0;

  const threat =
    fake > 5 ? "HIGH" :
      fake > 2 ? "MEDIUM" :
        "LOW";

  const chartData = {
    labels: ["Fake", "Under Review", "Verified"],
    datasets: [{
      label: "Threat Distribution",
      data: [fake, review, verified],
      backgroundColor: ["#ef4444", "#f59e0b", "#22c55e"]
    }]
  };

  return (
    <div className={`app ${theme}`}>

      <div className="sidebar">
        <h2>DISASTER AI</h2>

        <button onClick={() => setView("authority")}>Authority</button>
        <button onClick={() => setView("public")}>Public</button>

        <div className="theme-toggle">
          <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")}>
            {theme === "dark" ? "☀ Light Mode" : "🌙 Dark Mode"}
          </button>
        </div>
      </div>

      <div className="main">

        {view === "authority" && (
          <>
            <h1>Authority Monitoring Panel</h1>

            <div className="threat">
              Overall Threat Level:
              <span className={`threat-${threat.toLowerCase()}`}> {threat}</span>
            </div>

            <div className="stats">
              <div className="card red">Fake Posts<br />{fake}</div>
              <div className="card orange">Under Review<br />{review}</div>
              <div className="card green">Verified<br />{verified}</div>
              <div className="card blue">Avg Panic<br />{avgPanic}</div>
            </div>

            <div className="card">
              <Bar data={chartData} />
            </div>

            <h2>Heatmap</h2>
            <div className="card">
              <MapContainer center={[20.5937, 78.9629]} zoom={5} style={{ height: "300px" }}>
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {posts.map((p, i) => (
                  <Circle
                    key={i}
                    center={[17.385, 78.4867]}
                    radius={p.panic_index * 500}
                    pathOptions={{ color: "red", fillOpacity: 0.3 }}
                  />
                ))}
              </MapContainer>
            </div>

            <h2>Moderation Queue</h2>
            {posts.map(p => (
              p.status.includes("Review") && (
                <div key={p.id} className="queue">
                  <p>{p.text}</p>
                  <button onClick={() => approve(p.id)}>Approve</button>
                  <button onClick={() => reject(p.id)}>Reject</button>
                </div>
              )
            ))}
          </>
        )}

        {view === "public" && (
          <>
            <h1>Public Disaster Dashboard</h1>

            <div className="card">
              <h3>🚨 Emergency Helplines</h3>
              <p>🚑 108 - Ambulance</p>
              <p>🚓 100 - Police</p>
              <p>🚒 101 - Fire</p>
              <p>📞 1070 - Disaster Helpline</p>
            </div>

            <div className="card">
              <h3>📰 Official Updates</h3>
              <p>• Flood advisory issued in Hyderabad.</p>
              <p>• Temporary shelters opened in Secunderabad.</p>
              <p>• Emergency response teams deployed.</p>
            </div>

            <div className="card">
              <h3>🤖 Misinformation Checker</h3>
              <textarea
                placeholder="Enter suspicious disaster news..."
                value={text}
                onChange={e => setText(e.target.value)}
              />
              <button onClick={analyzeText}>Analyze</button>

              {result && (
                <div className="result">
                  <p>Status: {result.status}</p>
                  <p>Credibility: {result.credibility_score}/100</p>
                  <p>Panic Index: {result.panic_index}/100</p>
                  <p>Detected Language: {result.language}</p>
                </div>
              )}
            </div>
          </>
        )}

      </div>
    </div>
  );
}

export default App;