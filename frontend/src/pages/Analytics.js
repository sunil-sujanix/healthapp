import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function Analytics() {
  const [data, setData] = useState([]);
  const token = localStorage.getItem("token");

  useEffect(() => {
    fetch("http://localhost:5000/analytics/bp_trend", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((d) => setData(d));
  }, []);

  return (
    <div className="analytics">
      <h2>Blood Pressure Trend</h2>
      <LineChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="sys" stroke="#8884d8" />
        <Line type="monotone" dataKey="dia" stroke="#82ca9d" />
      </LineChart>
    </div>
  );
}
