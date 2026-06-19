import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Diagnose from "./pages/Diagnose.jsx";
import History from "./pages/History.jsx";
import Catalog from "./pages/Catalog.jsx";
import Auth from "./pages/Auth.jsx";
import "./styles.css";

function App() {
  return (
    <BrowserRouter>
      <nav className="nav">
        <span className="brand">LeafGuard</span>
        <div className="nav-links">
          <Link to="/">Diagnose</Link>
          <Link to="/history">History</Link>
          <Link to="/catalog">Catalog</Link>
          <Link to="/auth">Account</Link>
        </div>
      </nav>
      <main className="container">
        <Routes>
          <Route path="/" element={<Diagnose />} />
          <Route path="/history" element={<History />} />
          <Route path="/catalog" element={<Catalog />} />
          <Route path="/auth" element={<Auth />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
