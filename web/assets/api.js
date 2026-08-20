const SentinelAPI = (() => {
  const key = "sentinelcore_api_base";
  const tokenKey = "sentinelcore_access_token";

  function base() {
    return localStorage.getItem(key) || "/api/v1";
  }
  function token() {
    return localStorage.getItem(tokenKey) || "";
  }
  async function request(path, options = {}) {
    const headers = {"Accept":"application/json", ...(options.headers || {})};
    const t = token();
    if (t) headers.Authorization = `Bearer ${t}`;
    const response = await fetch(`${base()}${path}`, {
      ...options, headers, credentials: "include"
    });
    if (!response.ok) {
      const text = await response.text();
      throw new Error(`${response.status}: ${text || response.statusText}`);
    }
    return response.status === 204 ? null : response.json();
  }
  return {
    get base(){ return base(); },
    setBase(url){ localStorage.setItem(key, url.replace(/\/+$/,"")); },
    setToken(value){ localStorage.setItem(tokenKey, value); },
    clearToken(){ localStorage.removeItem(tokenKey); },
    request,
    health(){ return request("/health"); },
    metrics(){ return request("/dashboard/metrics"); },
    incidents(){ return request("/incidents?limit=10"); },
    events(){ return request("/events?limit=20"); },
    agents(){ return request("/agents?limit=20"); }
  };
})();
