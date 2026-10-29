// ops/bitunix-shadow-read-proxy.mjs
import http from "node:http";
import { timingSafeEqual } from "node:crypto";

// lib/bitunix-shadow.ts
var SHADOW_ACCOUNTS = [
  { id: "prototype", name: "Prototype Bitunix + Phoenix", description: "Diamants imm\xE9diats \xB7 autres entr\xE9es confirm\xE9es" },
  { id: "original", name: "RAFALE2 Bitunix + Phoenix \u2014 entr\xE9es originales", description: "Entr\xE9es originales imm\xE9diates" }
];
var metricKeys = ["initialCapitalUsd", "accountValueUsd", "cashUsd", "floatingPnlUsd", "pnlTotalUsd", "pnlTotalPct", "pnl24hUsd", "pnl24hPct", "pnl7dUsd", "pnl7dPct", "pnl14dUsd", "pnl14dPct", "pnl30dUsd", "pnl30dPct", "drawdownPct", "maxDrawdownPct", "highWaterUsd", "pf", "winRatePct", "expectancyR", "closedTrades", "wins", "losses", "grossProfitUsd", "grossLossUsd", "feesUsd", "fundingUsd", "positionsOpen", "notionalUsd", "marginUsedUsd", "marginPct", "maxMarginPct", "openRiskPct", "maxOpenRiskPct", "pendingConfirmations"];
var positionNumbers = ["entry", "mark", "stop", "qty", "notional", "riskPct", "leverage", "margin", "unrealized", "funding"];
var tradeNumbers = ["entryTime", "exitTime", "entry", "exit", "stop", "qty", "notional", "riskCash", "riskPct", "targetRiskPct", "leverage", "margin", "entryFee", "exitFee", "fees", "funding", "grossPnl", "pnl", "R"];
var phoenixNumbers = ["factor", "drawdownPct", "episodeDays", "healthR", "healthN", "fastHealthR", "fastN", "recovery", "alignedMedian24", "at"];
var obj = (x) => x && typeof x === "object" && !Array.isArray(x) ? x : {};
var finite = (x) => typeof x === "number" && Number.isFinite(x) ? x : null;
var str = (x) => typeof x === "string" ? x : null;
var numbers = (x, keys) => Object.fromEntries(keys.map((k) => [k, finite(x[k])]));
function parseBitunixShadow(input) {
  const data = obj(input);
  if (data.virtual !== true || data.liveOrderCapability !== false || !Array.isArray(data.variants) || data.variants.length !== 2) throw new Error("INVALID_SHADOW_DATA");
  if (typeof data.generatedAt !== "string" || !Number.isFinite(Date.parse(data.generatedAt))) throw new Error("INVALID_SHADOW_TIME");
  const ids = data.variants.map((x) => obj(x).id);
  if (new Set(ids).size !== 2 || !SHADOW_ACCOUNTS.every((a) => ids.includes(a.id))) throw new Error("INVALID_SHADOW_VARIANTS");
  const sourceVariants = data.variants;
  const variants = SHADOW_ACCOUNTS.map(({ id }) => {
    const v = obj(sourceVariants.find((x) => obj(x).id === id));
    if (v.virtual !== true || v.liveOrderCapability !== false || v.venue !== "BITUNIX" || !Array.isArray(v.positions) || !Array.isArray(v.recentTrades)) throw new Error("INVALID_SHADOW_ACCOUNT");
    const metrics = numbers(v, metricKeys);
    if (metrics.initialCapitalUsd !== 1e3 || metrics.accountValueUsd === null || metrics.positionsOpen !== v.positions.length) throw new Error("INCONSISTENT_SHADOW_ACCOUNT");
    const positions = v.positions.map((x) => {
      const p2 = obj(x);
      return { ...numbers(p2, positionNumbers), coin: str(p2.coin), symbol: str(p2.symbol), direction: str(p2.direction), quality: str(p2.quality) };
    });
    const recentTrades = v.recentTrades.map((x) => {
      const t = obj(x), n = numbers(t, tradeNumbers);
      return { ...n, id: str(t.id), coin: str(t.coin), symbol: str(t.symbol), direction: str(t.direction), reason: str(t.reason), quality: str(t.quality), diamond: t.diamond === true, pnlPctNotional: n.pnl !== null && n.notional !== null && n.notional > 0 ? 100 * n.pnl / n.notional : null };
    });
    const p = obj(v.phoenix), model = obj(v.executionModel);
    return {
      ...metrics,
      id,
      virtual: true,
      liveOrderCapability: false,
      venue: "BITUNIX",
      lastUpdateUtc: str(v.lastUpdateUtc),
      version: str(v.version),
      positions,
      recentTrades,
      stopsVisible: positions.filter((p2) => p2.stop !== null && p2.stop > 0).length,
      phoenix: { ...numbers(p, phoenixNumbers), active: typeof p.active === "boolean" ? p.active : null, override: str(p.override) },
      executionModel: { marginMode: str(model.marginMode), feesPerSide: finite(model.feesPerSide), orderBookVwap: typeof model.orderBookVwap === "boolean" ? model.orderBookVwap : null, funding: typeof model.funding === "boolean" ? model.funding : null, stopTrigger: str(model.stopTrigger), confirmation: str(model.confirmation) }
    };
  });
  return { variants, generatedAt: data.generatedAt, market: { lastPoll: finite(obj(data.market).lastPoll), degraded: !!obj(data.market).lastError || obj(data.market).degraded === true }, virtual: true, liveOrderCapability: false };
}

// ops/bitunix-shadow-read-proxy.mjs
var UPSTREAM = "https://philbot-bitunix-phoenix-shadow-v1-production.up.railway.app/control";
var accessToken = process.env.CONTROL_PROXY_TOKEN || "";
var upstreamToken = process.env.UPSTREAM_SHADOW_TOKEN || "";
if (accessToken.length < 32 || !upstreamToken) throw new Error("Required read-only authentication configuration is missing");
function valid(value) {
  const a = Buffer.from(typeof value === "string" ? value : ""), b = Buffer.from(accessToken);
  return a.length === b.length && timingSafeEqual(a, b);
}
var cached = null;
var cachedAt = 0;
var inFlight = null;
async function control() {
  if (cached && Date.now() - cachedAt < 5e3) return cached;
  if (inFlight) return inFlight;
  inFlight = (async () => {
    const response = await fetch(UPSTREAM, { method: "GET", headers: { Accept: "application/json", "x-shadow-token": upstreamToken }, redirect: "error", signal: AbortSignal.timeout(1e4) });
    if (!response.ok) throw new Error("Upstream unavailable");
    const text = await response.text();
    if (text.length > 2e6) throw new Error("Oversized response");
    cached = parseBitunixShadow(JSON.parse(text));
    cachedAt = Date.now();
    return cached;
  })().finally(() => {
    inFlight = null;
  });
  return inFlight;
}
function send(res, status, payload) {
  res.writeHead(status, { "content-type": "application/json", "cache-control": "private, no-store", "x-content-type-options": "nosniff" });
  res.end(JSON.stringify(payload));
}
http.createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/healthz") return send(res, 200, { ok: true, service: "philbot-control-shadow-read-proxy", readOnly: true });
  if (req.method !== "GET" || req.url !== "/control") return send(res, 404, { error: "NOT_FOUND" });
  if (!valid(req.headers["x-control-read-token"])) return send(res, 401, { error: "UNAUTHORIZED" });
  try {
    return send(res, 200, await control());
  } catch {
    return send(res, 502, { error: "SHADOW_UNAVAILABLE" });
  }
}).listen(Number(process.env.PORT || 8080), "::");
