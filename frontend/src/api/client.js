// Central API client. Token persisted in memory + localStorage.
const BASE = "/api/v1";

function authHeaders() {
  const token = localStorage.getItem("lg_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function register(email, password, fullName) {
  const res = await fetch(`${BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name: fullName }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Registration failed");
  return res.json();
}

export async function login(email, password) {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form,
  });
  if (!res.ok) throw new Error("Invalid credentials");
  const data = await res.json();
  localStorage.setItem("lg_token", data.access_token);
  return data;
}

export function logout() {
  localStorage.removeItem("lg_token");
}

export async function predict(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/diagnosis/predict`, {
    method: "POST",
    headers: { ...authHeaders() },
    body: form,
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Prediction failed");
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${BASE}/diagnosis/history`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Could not load history");
  return res.json();
}

export async function listDiseases() {
  const res = await fetch(`${BASE}/diseases`);
  if (!res.ok) throw new Error("Could not load catalog");
  return res.json();
}

export async function submitFeedback(payload) {
  const res = await fetch(`${BASE}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Feedback failed");
  return res.json();
}
