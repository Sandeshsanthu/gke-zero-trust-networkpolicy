const express = require("express");
const app = express();
const port = process.env.PORT || 8080;
function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
app.get("/work", async (req, res) => {
  const delayMs = parseInt(process.env.DELAY_MS || "0", 10);
  const failPct = Math.max(0, Math.min(100, parseInt(process.env.FAIL_PCT || "0", 10)));
  if (delayMs > 0) await sleep(delayMs);
  const roll = Math.random() * 100;
  if (roll < failPct) return res.status(503).json({ ok: false, error: "simulated-503" });
  res.json({ ok: true, service: "flaky-service", delayMs, failPct, ts: new Date().toISOString() });
});
app.get("/healthz", (req, res) => res.status(200).send("ok"));
app.listen(port, () => console.log(`flaky-service listening on ${port}`));
