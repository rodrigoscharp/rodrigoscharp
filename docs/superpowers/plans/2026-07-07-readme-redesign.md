# README Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the profile README's Featured Projects section from 2 to 5 entries, fix the stale BETO-IA link, refresh the About paragraph, and upgrade project tags to icon badges — without touching the Stats/snake/typing-SVG widgets that already work.

**Architecture:** Single-file change to `README.md`. No build step, no tests-as-code — "testing" here means verifying every image/badge URL used returns HTTP 200 and every project/demo link resolves, then eyeballing the rendered Markdown.

**Tech Stack:** Markdown, [skillicons.dev](https://skillicons.dev) icon badges, [shields.io](https://img.shields.io) custom badges.

## Global Constraints

- README content stays in **English** (spec: "Idioma do README permanece inglês").
- Keep the existing typing SVG header, Stack section, Stats section, and footer **unchanged** — do not modify those blocks.
- Do **not** add a "Building Now" section (explicitly out of scope per spec).
- Do **not** change the Stats widgets or self-host anything (explicitly out of scope per spec — accept `github-readme-stats.vercel.app` intermittent 503s as-is).
- Final Featured Projects order is exactly: **Athena Matching Engine → WalletCore → BETO-IA → HelpNote-IA → internet-banking-java**. All 5 use the same card format (no "top 3 + compact list" split).
- `gRPC` and `JWT` have no working skillicons.dev icon — represent them as plain shields.io badges (verified: skillicons.dev silently omits unsupported icons; shields.io renders a valid badge with or without a working logo slug, so it's still visually correct either way).
- Every skillicons.dev badge uses `&theme=dark`, matching the existing Stack section convention.

---

### Task 1: Update the About paragraph

**Files:**
- Modify: `README.md:15`

**Interfaces:** None (isolated text change).

- [ ] **Step 1: Replace the About paragraph**

Find this exact line in `README.md`:

```
Backend engineer from Brazil. I build production systems — from a high-performance financial matching engine processing **>100k orders/s** to an AI voice assistant that runs entirely on your own server. My core stack is **Java + Spring Boot**; I also ship full-stack when the job calls for it.
```

Replace it with:

```
Software engineer from Brazil. I build production systems across fintech, banking and AI — from a matching engine processing **>100k orders/s** to a digital wallet with double-entry ledger and an AI assistant that runs entirely on your own server. My core stack is **Java + Spring Boot**; I also ship full-stack when the job calls for it.
```

- [ ] **Step 2: Verify the change**

Run: `grep -n "Software engineer from Brazil" README.md`
Expected: one match, on line 15.

Run: `grep -c "Backend engineer from Brazil" README.md`
Expected: `0`

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Update About paragraph to reflect fintech/banking/AI breadth"
```

---

### Task 2: Replace the Featured Projects section with 5 cards

**Files:**
- Modify: `README.md:46-55` (the whole `## Featured Projects` block, from the heading down to the line before the closing `---`)

**Interfaces:** None (isolated section replacement). This task supersedes the old 2-card block entirely — order, links, and tag format all change together, so it is done as one edit rather than several partial ones.

- [ ] **Step 1: Replace the section**

Find this exact block in `README.md` (currently lines 46-55):

```
## Featured Projects

**[Own-Jarvis](https://github.com/rodrigoscharp/Own-Jarvis)**  
Privacy-first voice and text assistant that runs on your own server — no subscriptions, no data collection. Voice-activated with keyword detection, integrates with Spotify, Google Calendar, Gmail and GitHub. Powered by Groq LLaMA 3.1 with ElevenLabs TTS and a 3D animated particle orb interface.  
`Next.js 14` `TypeScript` `Groq` `ElevenLabs` `Supabase` `Vercel`

**[Athena Matching Engine](https://github.com/rodrigoscharp/Athena-Matching-Engine)**  
High-performance order matching engine for financial trading. Single-writer design using LMAX Disruptor achieves **>100k orders/s** throughput with **<10µs p50 latency**. Event sourcing + CQRS, hexagonal architecture, multi-protocol (REST, gRPC, WebSocket), full observability with Grafana dashboards.  
`Java 21` `Spring Boot 3` `Kafka` `Redis` `PostgreSQL` `gRPC`
```

Replace it with:

```
## Featured Projects

**[Athena Matching Engine](https://github.com/rodrigoscharp/Athena-Matching-Engine)**  
High-performance order matching engine for financial trading. Single-writer design using LMAX Disruptor achieves **>100k orders/s** throughput with **<10µs p50 latency**. Event sourcing + CQRS, hexagonal architecture, multi-protocol (REST, gRPC, WebSocket), full observability with Grafana dashboards.  
![](https://skillicons.dev/icons?i=java,spring,kafka,redis,postgres,docker&theme=dark) ![gRPC](https://img.shields.io/badge/gRPC-4285F4?style=flat-square)

**[WalletCore](https://github.com/rodrigoscharp/WalletCore)**  
Production-grade digital wallet REST API. Atomic transfers with double-entry ledger and pessimistic locking, JWT auth with rotating refresh tokens, exponential retry + dead-letter queue for resilience, idempotency keys, rate limiting, and Testcontainers-based integration tests (real Postgres + RabbitMQ, no mocks).  
![](https://skillicons.dev/icons?i=java,spring,postgres,redis,docker&theme=dark) ![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=flat-square&logo=rabbitmq&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)

**[BETO-IA](https://github.com/rodrigoscharp/BETO-IA)**  
Privacy-first voice and text assistant that runs on your own server — no subscriptions, no data collection. Voice-activated with keyword detection, integrates with Spotify, Google Calendar, Gmail and GitHub. Powered by Groq LLaMA 3.1 with ElevenLabs TTS and a 3D animated particle orb interface.  
![](https://skillicons.dev/icons?i=nextjs,ts,react,vercel,supabase&theme=dark) ![Groq](https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=groq&logoColor=white) ![ElevenLabs](https://img.shields.io/badge/ElevenLabs-000000?style=flat-square&logoColor=white)

**[HelpNote-IA](https://github.com/rodrigoscharp/HelpNote_-IA)** · [demo](https://help-note-ia.vercel.app)  
AI-powered note-taking assistant for lectures and technical talks. Transcribes audio, extracts keywords, classifies topics, and auto-generates complementary explanations to turn raw notes into structured, reviewable content.  
![](https://skillicons.dev/icons?i=js,java,html,css&theme=dark)

**[internet-banking-java](https://github.com/rodrigoscharp/internet-banking-java)**  
Internet banking REST API with Spring Security-based authentication, JPA persistence and validation layer — core account and transaction operations over a relational MySQL backend.  
![](https://skillicons.dev/icons?i=java,spring,mysql,html,css,js&theme=dark)
```

- [ ] **Step 2: Verify every image/badge URL in the new section returns 200**

Run:

```bash
for url in \
  "https://skillicons.dev/icons?i=java,spring,kafka,redis,postgres,docker&theme=dark" \
  "https://img.shields.io/badge/gRPC-4285F4?style=flat-square" \
  "https://skillicons.dev/icons?i=java,spring,postgres,redis,docker&theme=dark" \
  "https://img.shields.io/badge/RabbitMQ-FF6600?style=flat-square&logo=rabbitmq&logoColor=white" \
  "https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white" \
  "https://skillicons.dev/icons?i=nextjs,ts,react,vercel,supabase&theme=dark" \
  "https://img.shields.io/badge/Groq-F55036?style=flat-square&logo=groq&logoColor=white" \
  "https://img.shields.io/badge/ElevenLabs-000000?style=flat-square&logoColor=white" \
  "https://skillicons.dev/icons?i=js,java,html,css&theme=dark" \
  "https://skillicons.dev/icons?i=java,spring,mysql,html,css,js&theme=dark" \
; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  echo "$code $url"
done
```

Expected: every line starts with `200`.

- [ ] **Step 3: Verify every project/demo link resolves**

Run:

```bash
for url in \
  "https://github.com/rodrigoscharp/Athena-Matching-Engine" \
  "https://github.com/rodrigoscharp/WalletCore" \
  "https://github.com/rodrigoscharp/BETO-IA" \
  "https://github.com/rodrigoscharp/HelpNote_-IA" \
  "https://help-note-ia.vercel.app" \
  "https://github.com/rodrigoscharp/internet-banking-java" \
; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L "$url")
  echo "$code $url"
done
```

Expected: every line starts with `200`.

- [ ] **Step 4: Confirm no stale reference remains**

Run: `grep -c "Own-Jarvis" README.md`
Expected: `0`

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Expand Featured Projects to 5 entries with icon badges, fix BETO-IA link"
```

---

### Task 3: Full-README verification pass

**Files:** None modified — this task only verifies the complete `README.md` (this task's change and Task 1/2's changes together).

**Interfaces:** None.

- [ ] **Step 1: Confirm the untouched sections are still intact**

Run: `grep -c "readme-typing-svg.demolab.com" README.md` — expected `1`
Run: `grep -c "github-readme-stats.vercel.app" README.md` — expected `2` (Stats + Top Langs)
Run: `grep -c "streak-stats.demolab.com" README.md` — expected `1`
Run: `grep -c "github-snake" README.md` — expected `3` (dark `<source>`, light `<source>`, and the `<img>` fallback tag for renderers without `<picture>`/`<source>` support — correction: an earlier version of this plan said `2` and omitted the fallback `<img>`, which caused an implementer to wrongly delete it; do not remove that line)

- [ ] **Step 2: Confirm section order**

Run: `grep -n "^## " README.md`
Expected output (line numbers will differ from the original since the file grew, but the order must match):

```
<N>:## Stack
<N>:## Featured Projects
<N>:## Stats
```

- [ ] **Step 3: Confirm Featured Projects card order**

Run: `grep -n "^\*\*\[" README.md`
Expected: 5 matches in this exact order — `Athena Matching Engine`, `WalletCore`, `BETO-IA`, `HelpNote-IA`, `internet-banking-java`.

- [ ] **Step 4: Render check**

Open `README.md` in a Markdown previewer (e.g. VS Code's built-in preview, or `gh repo view rodrigoscharp/rodrigoscharp --web` after pushing) and visually confirm:
- All 5 project cards show their icon badges (no broken-image icons).
- The About paragraph reads correctly and mentions "Software engineer".
- No leftover `Own-Jarvis` text or broken link anywhere on the page.

No commit expected for this task — it's a verification-only pass. If Step 1-3 reveal a discrepancy, fix it in the relevant section and commit with message `"Fix README verification issue: <what was wrong>"`.

---

## Self-Review Notes

- **Spec coverage:** About paragraph (Task 1) ✅. 5 Featured Projects in the specified order with the specified badges/descriptions/demo link (Task 2) ✅. BETO-IA link fix (Task 2, Step 1 + Step 4 grep check) ✅. gRPC/JWT-not-supported-by-skillicons handling (Task 2) ✅. Stack/Stats/header/footer left untouched (Task 3, Step 1) ✅. Out-of-scope items (Building Now, Stats self-host, top-3 split, other repos) — none of them appear anywhere in this plan ✅.
- **Placeholder scan:** No TBD/TODO; every step has literal content (exact old/new text, exact URLs, exact commands with expected output).
- **Type/name consistency:** Card titles and repo URLs used in Task 2 match the ones verified live via `curl`/GitHub API during design (BETO-IA redirect confirmed, HelpNote_-IA exact repo name with underscore-hyphen confirmed, help-note-ia.vercel.app confirmed reachable).
