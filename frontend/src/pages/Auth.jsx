import React, { useState } from "react";
import { login, register, logout } from "../api/client.js";

export default function Auth() {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [msg, setMsg] = useState(null);
  const loggedIn = !!localStorage.getItem("lg_token");

  async function submit() {
    setMsg(null);
    try {
      if (mode === "register") {
        await register(email, password, fullName);
        setMsg("Registered. You can now log in.");
        setMode("login");
      } else {
        await login(email, password);
        setMsg("Logged in.");
      }
    } catch (e) {
      setMsg(e.message);
    }
  }

  if (loggedIn) {
    return (
      <section>
        <h1>Account</h1>
        <p>You are logged in.</p>
        <button onClick={() => { logout(); setMsg("Logged out."); }}>Log out</button>
        {msg && <p className="muted">{msg}</p>}
      </section>
    );
  }

  return (
    <section>
      <h1>{mode === "login" ? "Log In" : "Register"}</h1>
      {mode === "register" && (
        <input placeholder="Full name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
      )}
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={submit}>{mode === "login" ? "Log in" : "Register"}</button>
      <button className="link" onClick={() => setMode(mode === "login" ? "register" : "login")}>
        {mode === "login" ? "Need an account? Register" : "Have an account? Log in"}
      </button>
      {msg && <p className="muted">{msg}</p>}
    </section>
  );
}
