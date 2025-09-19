import { useState, useEffect } from "react";
import "./Dashboard.css"; // optional CSS file for styling

export default function Dashboard() {
  const [deps, setDeps] = useState([]);
  const [depName, setDepName] = useState("");
  const [records, setRecords] = useState([]);
  const token = localStorage.getItem("token");

  // 🔹 Fetch dependents
  const fetchDeps = async () => {
    const res = await fetch("http://localhost:5000/deps", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await res.json();
    setDeps(data.data || []);
  };

  // 🔹 Add a dependent
  const addDep = async () => {
    if (!depName.trim()) return;
    await fetch("http://localhost:5000/deps", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ name: depName }),
    });
    setDepName("");
    fetchDeps();
  };

  // 🔹 Fetch records for one dependent
  const fetchRecords = async (depId) => {
    const res = await fetch(`http://localhost:5000/records?dependent_id=${depId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = await res.json();
    setRecords(data);
  };

  // 🔹 Add a record with file upload
  const addRecord = async (depId, file) => {
    const form = new FormData();
    form.append("dependent_id", depId);
    form.append("kind", "prescription");
    if (file) form.append("file", file);

    await fetch("http://localhost:5000/records", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: form,
    });
    fetchRecords(depId);
  };

  useEffect(() => {
    fetchDeps();
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>

      <div className="section">
        <h3>Dependents</h3>
        <ul>
          {deps.map((d) => (
            <li key={d.id} onClick={() => fetchRecords(d.id)}>
              {d.name} ({d.relationship})
            </li>
          ))}
        </ul>
        <div className="add-box">
          <input
            value={depName}
            onChange={(e) => setDepName(e.target.value)}
            placeholder="Add dependent"
          />
          <button onClick={addDep}>Add</button>
        </div>
      </div>

      <div className="section">
        <h3>Records</h3>
        <ul>
          {records.map((r) => (
            <li key={r.id}>
              {r.kind} - {new Date(r.taken_at).toLocaleString()}
            </li>
          ))}
        </ul>
        {deps.length > 0 && (
          <div className="upload-box">
            <label>Upload file for {deps[0].name}:</label>
            <input
              type="file"
              onChange={(e) => addRecord(deps[0].id, e.target.files[0])}
            />
          </div>
        )}
      </div>
    </div>
  );
}
