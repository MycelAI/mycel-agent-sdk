---
search:
  exclude: true
---

# Agent framework & gateway market pains (2026 synthesis)

This note captures **recurring themes** from public sources (GitHub issues on
agent frameworks, gateway/control-plane writing, MCP governance articles, and
framework-complexity discussions). It is **not** a primary-source scrape of
social threads; treat **observed theme** vs **hypothesis** as labeled below.

**Product context:** [Mycel Agent SDK](https://github.com/MycelAI/mycel-agent-sdk)
— Python fork of OpenAI Agents SDK, **gateway-first** routing, **LiteLLM
removed** from the distribution, built-in tools + **permission modes**, optional
Rust accelerator, bundled prompts / eval harness.

---

## 1. Pain points (ranked by inferred frequency × severity)

| Rank | Pain | Notes |
| --- | --- | --- |
| 1 | **Observability / “control plane”** | **Observed:** Widespread demand for centralized spend, tracing, and request attribution across LLM + tools; MCP writeups on weak agent-side observability. Teams need to answer *who spent what, on which tool path, with what outcome*. |
| 2 | **Production safety** | **Observed:** MCP auth and governance posts (credential scope, confused-deputy class concerns, fragmented audit). Aligns with **Claude/Cursor-style** explicit permission UX expectations for coding agents. |
| 3 | **Cost + routing discipline** | **Observed:** Practitioner and vendor content on uncontrolled routing (“everything to the most expensive model”), missing budgets/quotas, need for fallback policies. |
| 4 | **Latency, reliability, dependency weight** | **Observed:** Upstream agents-Python issues around tracing/import/fork ergonomics; broader critiques of **heavy optional stacks** (specific LiteLLM benchmark claims should be treated as **hypothesis** / verify per release). |
| 5 | **Memory / lifecycle / long-run jobs** | **Observed:** Upstream issue class around **agent references**, `RunItem` retention, and **state between turns** — long conversations and auditing strain RAM or developer ergonomics. |
| 6 | **Streaming + tool loops** | **Observed:** Maintenance burden when streamed and non-streamed paths diverge; users feel pain when events are incomplete or inconsistent (this repo’s own contributor docs emphasize keeping paths aligned). |
| 7 | **Vendor lock-in and migration** | **Hypothesis:** High concern over Responses vs Chat Completions, provider-specific tool schemas, and rewrites when models change; gateway-shaped APIs **reduce** but do not remove this. |
| 8 | **MCP at scale** | **Observed:** Enterprise MCP pieces stress **patchwork auth** and **multi-tenant** gaps — **hypothesis** this is acute for regulated EU buyers. |
| 9 | **Evals and regression** | **Observed:** General MLOps gap; market under-serves **agent evals tied to production tool traces** (not mocks only). |
| 10 | **Framework complexity** | **Observed:** Discourse on steep learning curves for large orchestration frameworks — **hypothesis** many teams want **thin** handoffs + tools, not graph-heavy setups. |
| 11 | **Realtime / telephony edge cases** | **Observed:** Niche by volume but **high severity** when production hits Realtime + tools + carrier/config constraints. |
| 12 | **Supply-chain trust** | **Observed:** 2026 **PyPI ecosystem incidents** elevate “what’s in `pip install`” — **hypothesis** pushes buyers toward **smaller dependency surfaces** or **owned gateways**. |

---

## 2. Fit vs Mycel positioning

### Likely **reduces** pain

- **Gateway-first, keys at the edge:** Control plane, cost attribution, fewer scattered provider adapters in app code.
- **LiteLLM out of the distribution:** Smaller opinionated path; appeals after heavy transitive trust incidents (**buyer story — not universal**).
- **Built-in tools + `PermissionMode`:** Directly targets tool safety and product-like agent UX.
- **OpenAI-native wire + Chat Completions gateway:** Can lower *some* lock-in vs provider-only SDKs if gateway normalizes errors and schemas (**depends on gateway parity**).
- **Bundled prompts + eval harness:** Addresses trace/regression testing beyond mocks.
- **Rust gateway / optional accelerator:** Speaks to latency and hot paths (**implementation-dependent** until benchmarked in target workloads).

### Likely **creates** friction

- **Fork divergence:** SemVer and behaviour can drift from upstream — **upgrade tax** and security-patch alignment worry enterprises.
- **No LiteLLM in-box:** Teams standardized on LiteLLM routing/ops dashboards may need **re-platforming** (**observed** pattern: orgs anchor on one router).
- **Gateway operations:** Complexity moves to an HTTP service — without reference IaC or managed story, some teams see a **new failure domain** (**hypothesis**).
- **EU/regulated positioning:** Needs documented flows (data residency, retention, tenant isolation), not slogans (**hypothesis**).
- **MCP enterprise gaps** are not fully solved by a Python SDK alone without tenant-aware patterns (**observed** governance gap).

---

## 3. Testable product / feature hypotheses

1. **Gateway metering export:** Standard `x-trace-id`, token/cost headers or JSON extensions joinable from `RunResult` into **OpenTelemetry + billing**. *Test:* reproduce a cost spike from logs in under five minutes on a canary workload.
2. **Permission audit artifact:** Structured run manifest (tool, mode, allowlist decision) exportable to **SIEM** or object storage. *Test:* security review accepts for a sample workflow (**EU internal agents** narrative).
3. **Gateway compatibility matrix CI:** Automated matrix across **N** providers (errors, tool schemas, streaming deltas). *Test:* release blocked on matrix regressions.
4. **MCP enterprise profile:** Docs + optional helpers for **per-tenant MCP allowlists**, credential broker (Vault/KMS) patterns, confused-deputy guidance. *Test:* one reference multi-tenant deployment passes lightweight threat review.
5. **LiteLLM escape hatch (interop, not necessarily re-add):** Recipes to **migrate** or **bridge** existing LiteLLM deployments to the gateway. *Test:* measured **time-to-migrate** for a sample service.
6. **Long-run lifecycle presets:** First-class patterns for compaction, release of agent references, or checkpointed sessions. *Test:* 24h job RSS within budget vs baseline.
7. **Eval packs with denied-tool paths:** Golden traces including **denials**, not only happy paths. *Test:* CI catches regression in deny/allow logic.
8. **Incident + SBOM + fork CVE story:** Single procurement-facing doc: SBOM posture, how the fork tracks upstream security, gateway pinning/rollback. *Test:* shorter procurement questionnaire cycle (**hypothesis**).

---

## 4. Anti-patterns (agent platforms users push back on)

- **Black-box automation:** Unclear or non-replayable approvals (“bad CI/CD” trust drain).
- **Dashboards with no export:** Observability that does not join **OTel / Datadog / Grafana / SIEM**.
- **Magic routing:** Silent model swaps without SLOs or rollback paths.
- **Bloated install** for a hello-world agent: slow imports — feeds distrust of heavy stacks (**verify each release**).
- **Naive MCP demos:** Env-only secrets, no tenant boundary — production writeups call this out.
- **Stream vs non-stream inconsistency:** Erodes trust faster than missing features.
- **Fork without merge story:** Lag on upstream memory/tracing/realtime fixes reads as **double maintenance**.
- **Compliance washing:** “EU-ready” without data maps, subprocessors, retention, customer-controlled logging — procurement red flag (**hypothesis**).

---

## 5. Maintenance

- **Owner:** Mycel maintainers / product.  
- **Refresh cadence:** Revisit yearly or after major market incidents (supply chain, MCP spec shifts).  
- **Related in-repo:** [ExecPlan: gateway & Rust tiers](../execplans/mycel-fork-gateway-and-rust-tiers.md), [README](../../README.md).
