const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    throw new Error(payload?.message || "Request failed.");
  }

  return payload;
}

export function listKnowledgeBases() {
  return request("/knowledge-bases");
}

export function createKnowledgeBase(data) {
  return request("/knowledge-bases", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
