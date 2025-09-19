import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import "./App.css";

function App() {
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <BrowserRouter>
      <nav className="navbar">
        <h2>HealthTrack</h2>
        <div>
          {token && (
            <>
              <Link to="/">Dashboard</Link>
              <Link to="/analytics">Analytics</Link>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </>
          )}
          {!token && (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
      </nav>

      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={token ? <Dashboard /> : <Navigate to="/login" />} />

        <Route path="/analytics" element={token ? <Analytics /> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
