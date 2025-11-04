export async function apiFetch(path, options = {}) {
  // Build correct path + ensure trailing slash
  const cleanPath = path.endsWith("/") ? path : path + "/";
  const url = apiPath(cleanPath);

  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}
