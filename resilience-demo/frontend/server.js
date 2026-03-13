const express = require("express");
const axios = require("axios");
const app = express();
const port = process.env.PORT || 8080;
const upstreamBase = process.env.UPSTREAM_BASE || "http://flaky-service:8080";
app.get("/call", async (req, res) => {
  const timeoutMs = parseInt(process.env.APP_TIMEOUT_MS || "10000", 10);
  try {
    const r = await axios.get(`${upstreamBase}/work`, { timeout: timeoutMs });
    res.json({ ok: true, upstreamStatus: r.status, upstreamBody: r.data });
  } catch (e) {
    res.status(502).json({ ok: false, error: "upstream-call-failed", message: e.message });
  }
});
app.get("/healthz", (req, res) => res.status(200).send("ok"));
app.listen(port, () => console.log(`frontend listening on ${port}, upstream=${upstreamBase}`));
