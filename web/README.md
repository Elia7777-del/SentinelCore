# SentinelCore Web Dashboard

This is the responsive visual dashboard layer.

## Local test

From the `web` directory, use any static HTTP server, for example:

```bash
python -m http.server 8080
```

Then open `http://127.0.0.1:8080`.

## Production

Serve the static files over HTTPS behind the same authenticated deployment architecture as
the SentinelCore API. Replace demo metrics/event data with authenticated API calls before
using the dashboard with real security data.

The cyber background is generated with CSS (grid, gradients and lighting), so no copyrighted
stock image is required.
