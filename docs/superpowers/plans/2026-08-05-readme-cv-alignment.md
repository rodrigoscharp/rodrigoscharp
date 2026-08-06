# README CV Alignment & Awards Highlight — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the GitHub profile README so every claim matches the CV, the two national awards get prominent placement, and the Instagram creator presence is added — while keeping "Software Engineer" as the headline identity.

**Architecture:** A single file, `README.md`, rebuilt section by section in reading order. There is no build step, no test runner, and no application code. Each task replaces one contiguous block of the file and is verified by `grep` assertions plus a visual render check at the end. Tasks are ordered top-to-bottom through the document so line numbers stay predictable.

**Tech Stack:** GitHub-Flavored Markdown with inline HTML (`<div align="center">`, `<table>`, `<img>`). External image services: `readme-typing-svg.demolab.com`, `img.shields.io`, `skillicons.dev`. No CSS, no JavaScript, no dependencies.

## Global Constraints

- **Single file.** All changes land in `README.md` at the repo root. No new files, no workflows, no scripts.
- **Language: English.** Target audience is international recruiters.
- **GitHub-Flavored Markdown only.** No `<style>` tags, no `<script>`, no CSS. Centering uses `<div align="center">` and HTML tables, matching the existing file.
- **Every `<img>` must have an `alt` attribute.**
- **Badge style:** social/CTA badges use `style=for-the-badge`; the AI & LLM tech badges use `style=flat-square`.
- **No job title may appear as a heading or headline.** "Director", "CTO", and "Founder" must never head a section or appear in the typing SVG. Leadership and founding appear only inside prose describing delivered work.
- **Forbidden claims — must not appear anywhere in the final file:** `Disruptor`, `event sourcing`, `CQRS`, `single-writer`, `Grafana`, `10µs`, `p50`, `hexagonal`, `Testcontainers, no mocks` (the "no mocks" phrasing only; Testcontainers itself is allowed).
- **Canonical metrics, copied verbatim:**
  - Athena: `100k+ orders/s, sub-100µs p99`
  - Experience: `4+ years`
  - Government scale: `6+ systems serving 100,000+ citizens`
  - Awards: `two national awards`
- **Canonical email:** `rodrigosharp99@gmail.com` (note: no `c` before `harp` — this differs from the CV, and the README value is the one to use).
- **Canonical Instagram handle:** `@rodrigoscharp` → `https://instagram.com/rodrigoscharp`

---

## File Structure

| File | Responsibility |
|:---|:---|
| `README.md` | The entire deliverable. GitHub profile README, rendered at `github.com/rodrigoscharp`. |

No other file is created or modified.

The document's section order after this plan:

```
1. Header (typing SVG) + social badges      ← Task 1
2. About                                    ← Task 2
3. 🏆 Awards & Recognition                  ← Task 3
4. What I build best                        ← Task 4
5. Featured Projects                        ← Task 5
6. Tech I work with                         ← Task 6
7. CTA                                      ← Task 7
                                            ← Task 8: full-file verification
```

---

### Task 1: Header — typing SVG lines and social badges

**Files:**
- Modify: `README.md:1-12` (the opening `<div align="center">` block)

**Interfaces:**
- Consumes: nothing.
- Produces: the opening centered `<div>` containing the typing SVG and four badges. Task 7 reuses the LinkedIn URL `https://www.linkedin.com/in/rodrigoscharp/` and the Instagram URL `https://instagram.com/rodrigoscharp` defined here.

**Background:** `readme-typing-svg.demolab.com` renders an animated SVG. The rotating lines are passed in the `lines` query parameter, separated by `;`, and the whole value is URL-encoded. Encoding table for the characters used here:

| Character | Encoded |
|:---|:---|
| space | `+` |
| `'` (apostrophe) | `'` (safe, no encoding needed) |
| `,` | `%2C` |
| `·` (middle dot) | `%C2%B7` |
| `👋` (wave emoji) | `%F0%9F%91%8B` |
| `×` (multiplication sign) | `%C3%97` |
| `;` (line separator) | `;` (literal, do not encode) |

- [ ] **Step 1: Replace the header block**

Replace lines 1–12 of `README.md` (from `<div align="center">` through the closing `</div>`) with exactly this:

```html
<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=24&pause=1000&color=58A6FF&center=true&vCenter=true&width=640&lines=Hey%2C+I'm+Rodrigo+Scharp+%F0%9F%91%8B;Software+Engineer+%C2%B7+Brazil;Java+21+%2B+Spring+Boot+3;Systems+serving+100%2C000%2B+citizens;2%C3%97+National+Award+Winner" alt="Typing SVG" />

<br/>
<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rodrigoscharp/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:rodrigosharp99@gmail.com)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/rodrigoscharp)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rodrigoscharp)

</div>
```

- [ ] **Step 2: Verify the five typing lines are present and correctly encoded**

Run:

```bash
grep -c "Systems+serving+100%2C000%2B+citizens" README.md
grep -c "2%C3%97+National+Award+Winner" README.md
grep -c "Next.js+%2B+TypeScript" README.md
```

Expected: `1`, `1`, `0` — the first two lines are the new ones; the old `Next.js + TypeScript` and `Finance · AI · Full-stack` lines are gone from the header.

- [ ] **Step 3: Verify all four badges are present with correct colors**

Run:

```bash
grep -c "Instagram-E4405F?style=for-the-badge" README.md
grep -c "LinkedIn-0A66C2?style=for-the-badge" README.md
grep -c "Email-D14836?style=for-the-badge" README.md
grep -c "GitHub-181717?style=for-the-badge" README.md
```

Expected: `1` for each.

- [ ] **Step 4: Verify the canonical email**

Run:

```bash
grep -c "mailto:rodrigosharp99@gmail.com" README.md
grep -c "rodrigoscharp@gmail.com" README.md
```

Expected: `1` and `0`. The second grep catches the CV's variant spelling, which must not appear.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Update README header with award line and Instagram badge

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 2: About section

**Files:**
- Modify: `README.md` — the `### 👋 About me` heading and the paragraph beneath it

**Interfaces:**
- Consumes: the Instagram URL from Task 1.
- Produces: the `### 👋 About me` section. Task 3's Awards block is inserted directly after this section's trailing `<br/>`.

**Background:** The existing About section is a single paragraph positioning Rodrigo purely as a backend engineer. It is replaced by three paragraphs that add career scope (government scale, startup founding, awards) and the Instagram creator line — without naming any job title.

- [ ] **Step 1: Replace the About section**

Find the block starting with `### 👋 About me` and ending at the `<br/>` that precedes `### 🎯 What I do best`. Replace that whole block with:

```markdown
### 👋 About me

Software engineer from Brazil with **4+ years** building production systems across government, fintech and food-tech. I lead the technology team at the **Ubatuba city government**, where we've shipped **6+ systems serving 100,000+ citizens** — work recognized with **two national awards**. I also founded **MUNO**, a food-tech startup, where I built the backend and cloud infrastructure end to end.

My core stack is **Java 21 + Spring Boot 3**, and I go full-stack with **Next.js + TypeScript** when a product needs it. I care about the hard parts: correctness under concurrency, resilient architecture, and code that holds up in production rather than just in a demo.

Outside of engineering, I create content on programming, dev life and career as **[@rodrigoscharp](https://instagram.com/rodrigoscharp)** on Instagram.

<br/>
```

- [ ] **Step 2: Verify the CV facts landed**

Run:

```bash
grep -c "4+ years" README.md
grep -c "6+ systems serving 100,000+ citizens" README.md
grep -c "two national awards" README.md
grep -c "MUNO" README.md
grep -c "@rodrigoscharp\](https://instagram.com/rodrigoscharp)" README.md
```

Expected: `1` for each.

- [ ] **Step 3: Verify no job title leaked in**

Run:

```bash
grep -icE '\b(director|cto)\b' README.md
```

Expected: `0`. The word "founded" is a verb describing work and is allowed; "Founder" as a title is not, and this grep does not match "founded".

- [ ] **Step 4: Verify the old single-paragraph About is gone**

Run:

```bash
grep -c "focused on \*\*backend and distributed systems\*\*" README.md
```

Expected: `0`.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Rewrite README About with CV career scope and creator line

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 3: Awards & Recognition section

**Files:**
- Modify: `README.md` — insert a new section between About (Task 2) and `### 🎯 What I do best`

**Interfaces:**
- Consumes: the About section's closing `<br/>` from Task 2 as its insertion point.
- Produces: the `### 🏆 Awards & Recognition` section. Task 4 replaces the section that follows it.

**Background:** This is the highest-value new content — a national award is rare on a developer profile, so it sits above the projects. The award names are proper nouns: `Cidade Inovadora` is Portuguese and must **not** be translated.

- [ ] **Step 1: Insert the Awards section**

Insert this block immediately after the About section's trailing `<br/>` and immediately before `### 🎯 What I do best`:

```markdown
### 🏆 Awards & Recognition

<div align="center">

<table>
<tr>
<td width="50%" valign="top">

🏆 <b>Smart City Award</b>

National recognition for digital transformation and smart city initiatives at Prefeitura de Ubatuba.

</td>
<td width="50%" valign="top">

🏆 <b>Cidade Inovadora Award</b>

National recognition for innovation in public administration and technology-driven municipal governance.

</td>
</tr>
</table>

</div>

<br/>
```

- [ ] **Step 2: Verify both awards are present with exact names**

Run:

```bash
grep -c "Smart City Award" README.md
grep -c "Cidade Inovadora Award" README.md
grep -c "Prefeitura de Ubatuba" README.md
```

Expected: `1` for each.

- [ ] **Step 3: Verify the section sits above the projects**

Run:

```bash
awk '/^### 🏆 Awards/{a=NR} /^### 🎯/{b=NR} END{print (a>0 && b>0 && a<b) ? "OK" : "WRONG ORDER"}' README.md
```

Expected: `OK`.

- [ ] **Step 4: Verify the HTML table is balanced**

Run:

```bash
echo "open=$(grep -c '<table>' README.md) close=$(grep -c '</table>' README.md)"
```

Expected: `open` and `close` are equal (`open=2 close=2` at this point — one table here, one in the existing tech stack section).

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Add Awards & Recognition section to README

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 4: "What I build best" section

**Files:**
- Modify: `README.md` — replace the `### 🎯 What I do best` section entirely

**Interfaces:**
- Consumes: the Awards section from Task 3 as the preceding block.
- Produces: the `### 🎯 What I build best` section (note: heading text changes from "do" to "build"). Task 5 inserts the Featured Projects section after this one.

**Background:** The existing bullets contain three claims Rodrigo confirmed he has never used — LMAX Disruptor, event sourcing, CQRS — plus a Grafana/observability bullet and a "hexagonal architecture" mention that appear nowhere in the CV. Every bullet below traces to a specific CV line.

- [ ] **Step 1: Replace the section**

Replace the block from `### 🎯 What I do best` through the `<br/>` preceding `### 🧰 Tech I work with` with:

```markdown
### 🎯 What I build best

- **Systems at public scale** — 6+ government systems in production, serving 100,000+ citizens.
- **Financial engineering** — double-entry ledgers, order matching (**100k+ orders/s, sub-100µs p99**), atomic transfers with pessimistic locking, and idempotency.
- **Distributed architecture** — REST · gRPC · WebSocket services, event-driven with RabbitMQ and Kafka, clean architecture.
- **Resilience & reliability** — retries with backoff, dead-letter queues, rate limiting, and integration tests with Testcontainers.
- **AI & LLM integration** — voice and text assistants powered by Groq LLaMA and ElevenLabs, self-hosted and privacy-first.
- **Cloud & DevOps** — AWS (ECS, ALB, CloudFront, API Gateway, Lambda), Docker, and CI/CD pipelines.

<br/>
```

- [ ] **Step 2: Verify the forbidden claims are gone**

Run:

```bash
grep -icE 'disruptor|event sourcing|cqrs|single-writer|grafana|hexagonal' README.md
```

Expected: `0`.

- [ ] **Step 3: Verify the old metric is gone and the canonical one is present**

Run:

```bash
grep -icE '10µs|p50' README.md
grep -c "100k+ orders/s, sub-100µs p99" README.md
```

Expected: `0` and `1`.

- [ ] **Step 4: Verify the six bullets and the renamed heading**

Run:

```bash
grep -c "^### 🎯 What I build best" README.md
grep -c "^- \*\*" README.md
```

Expected: `1` and `6`.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Rewrite capabilities section with CV-backed claims only

Removes LMAX Disruptor, event sourcing, CQRS, hexagonal architecture and
Grafana claims that are not in the CV. Corrects the Athena latency metric
to 100k+ orders/s, sub-100µs p99.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 5: Featured Projects section

**Files:**
- Modify: `README.md` — insert a new section after "What I build best" (Task 4) and before `### 🧰 Tech I work with`

**Interfaces:**
- Consumes: the trailing `<br/>` from Task 4 as its insertion point.
- Produces: the `### 🚀 Featured Projects` section. Task 7 removes the now-redundant "My featured work is pinned below" line.

**Background:** The current README tells recruiters to scroll to the pinned repos. That costs a click and relies on GitHub's pin ordering. A table states the projects, what they do, and their stack up front. Repo URLs are taken verbatim from the CV — note `HelpNote_-IA` has an underscore *and* a hyphen; that is the actual repo name.

- [ ] **Step 1: Insert the Featured Projects section**

Insert immediately after the `<br/>` closing Task 4's section, and immediately before `### 🧰 Tech I work with`:

```markdown
### 🚀 Featured Projects

| Project | What it is | Stack |
|:---|:---|:---|
| **[WalletCore](https://github.com/rodrigoscharp/WalletCore)** | Digital wallet API — double-entry ledger, JWT auth, pessimistic locking for concurrency safety, async notifications | Java 21 · Spring Boot 3 · PostgreSQL · RabbitMQ · Redis |
| **[Athena Matching Engine](https://github.com/rodrigoscharp/Athena-Matching-Engine)** | Order matching engine for financial markets — 100k+ orders/s, sub-100µs p99, lock-free concurrency design | Java 21 · Spring Boot · Kafka · Redis · gRPC |
| **[BETO IA](https://github.com/rodrigoscharp/BETO-IA)** | Self-hosted voice AI assistant — Spotify, Google Calendar and GitHub integrations, no third-party subscriptions | Next.js 14 · TypeScript · Groq · ElevenLabs · Supabase |
| **[HelpNote IA](https://github.com/rodrigoscharp/HelpNote_-IA)** | Transcribes lecture and event audio, extracts keywords, and generates enriched summaries | Java · Spring Boot · PostgreSQL · LLM |

<br/>
```

- [ ] **Step 2: Verify all four repo URLs are exact**

Run:

```bash
grep -c "github.com/rodrigoscharp/WalletCore" README.md
grep -c "github.com/rodrigoscharp/Athena-Matching-Engine" README.md
grep -c "github.com/rodrigoscharp/BETO-IA" README.md
grep -c "github.com/rodrigoscharp/HelpNote_-IA" README.md
```

Expected: `1` for each.

- [ ] **Step 3: Verify the table has exactly four project rows**

Run:

```bash
grep -c "^| \*\*\[" README.md
```

Expected: `4`.

- [ ] **Step 4: Verify the section order**

Run:

```bash
awk '/^### 🎯/{a=NR} /^### 🚀/{b=NR} /^### 🧰/{c=NR} END{print (a<b && b<c) ? "OK" : "WRONG ORDER"}' README.md
```

Expected: `OK`.

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "Add Featured Projects table to README

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 6: Tech stack — add AWS

**Files:**
- Modify: `README.md` — the `Data &amp; Infra` row of the skillicons table

**Interfaces:**
- Consumes: the existing `### 🧰 Tech I work with` table, unchanged from the current file.
- Produces: nothing new. This is the smallest change in the plan.

**Background:** The CV lists AWS (CloudFront, ALB, ECS, API Gateway, Lambda) under Cloud & DevOps, and Task 4 now claims AWS in a bullet — the icon row must match. `skillicons.dev` takes a comma-separated `i=` parameter; `aws` is a valid slug. RabbitMQ has no skillicons slug and is intentionally not added here; it is already covered in Task 4's bullets and Task 5's WalletCore row.

- [ ] **Step 1: Add `aws` to the Data & Infra icon row**

Find this line:

```html
<td><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=postgres,mysql,redis,kafka,docker&theme=dark" alt="Data and Infra" /></a></td>
```

Replace it with:

```html
<td><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=postgres,mysql,redis,kafka,docker,aws&theme=dark" alt="Data and Infra" /></a></td>
```

- [ ] **Step 2: Verify the icon list**

Run:

```bash
grep -c "i=postgres,mysql,redis,kafka,docker,aws&theme=dark" README.md
grep -c "i=postgres,mysql,redis,kafka,docker&theme=dark" README.md
```

Expected: `1` and `0`.

- [ ] **Step 3: Verify the other three icon rows are untouched**

Run:

```bash
grep -c "i=java,spring,nodejs&theme=dark" README.md
grep -c "i=nextjs,ts,react&theme=dark" README.md
grep -c "ElevenLabs" README.md
```

Expected: `1`, `1`, and at least `1`.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "Add AWS to README tech stack icons

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 7: Closing CTA

**Files:**
- Modify: `README.md` — the final centered `<div>`, currently containing the "pinned below" line and a single LinkedIn badge

**Interfaces:**
- Consumes: the LinkedIn and Instagram URLs from Task 1; the Featured Projects section from Task 5, which makes the "pinned below" line redundant.
- Produces: the final block of the file.

**Background:** The current closing block says `<i>📌 My featured work is pinned below.</i>`. Task 5 put the projects in the document itself, so that line is now false — it points readers past the end of the README. It is removed and replaced with two CTA badges.

- [ ] **Step 1: Replace the closing block**

Replace the final centered `<div>` (from the `<div align="center">` that contains `📌 My featured work is pinned below.` through the file's last `</div>`) with:

```html
<div align="center">

[![Let's connect](https://img.shields.io/badge/Let's_connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rodrigoscharp/)
[![Follow my content](https://img.shields.io/badge/Follow_my_content-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/rodrigoscharp)

</div>
```

- [ ] **Step 2: Verify the stale pinned-work line is gone**

Run:

```bash
grep -c "pinned below" README.md
```

Expected: `0`.

- [ ] **Step 3: Verify both CTA badges are present**

Run:

```bash
grep -c "Let's_connect-0A66C2" README.md
grep -c "Follow_my_content-E4405F" README.md
```

Expected: `1` for each.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "Replace README closing CTA with LinkedIn and Instagram badges

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

### Task 8: Full-file verification

**Files:**
- Modify: `README.md` only if a check fails.

**Interfaces:**
- Consumes: the complete file produced by Tasks 1–7.
- Produces: nothing. This task is the spec's Verification section, run as a gate.

**Background:** Tasks 1–7 each verified their own block. This task runs the spec's six verification items against the whole document, catching anything a per-task grep missed — a duplicated section, an unbalanced tag, an `<img>` that lost its `alt`.

- [ ] **Step 1: Run the forbidden-claims sweep**

Run:

```bash
grep -inE 'disruptor|event sourcing|cqrs|single-writer|grafana|hexagonal|10µs|p50|rodrigoscharp@gmail' README.md; echo "exit=$?"
```

Expected: no matching lines printed, `exit=1` (grep's "no match" status). Any printed line is a failure — remove the offending claim.

- [ ] **Step 2: Verify every canonical fact is present exactly once**

Run:

```bash
for s in "4+ years" \
         "6+ systems serving 100,000+ citizens" \
         "two national awards" \
         "100k+ orders/s, sub-100µs p99" \
         "Smart City Award" \
         "Cidade Inovadora Award" \
         "instagram.com/rodrigoscharp" ; do
  printf '%-45s %s\n' "$s" "$(grep -cF "$s" README.md)"
done
```

Expected: `1` for every row, with two deliberate exceptions:

- `100k+ orders/s, sub-100µs p99` is `2` — Task 4 puts it in the capabilities bullet and Task 5 puts it in the Athena project row. Both are required; the two must stay byte-identical, which is the point of checking it here.
- `instagram.com/rodrigoscharp` is `3` — header badge, About prose link, CTA badge.

- [ ] **Step 3: Verify no job title appears as a heading or in the header**

Run:

```bash
grep -inE '^#+.*(director|cto|founder)|lines=.*(Director|CTO|Founder)' README.md; echo "exit=$?"
```

Expected: no lines printed, `exit=1`.

- [ ] **Step 4: Verify every `<img>` has an alt attribute**

Run:

```bash
total=$(grep -o '<img ' README.md | wc -l | tr -d ' ')
withalt=$(grep -o '<img [^>]*alt=' README.md | wc -l | tr -d ' ')
echo "img=$total with_alt=$withalt"
```

Expected: `img` and `with_alt` are equal.

- [ ] **Step 5: Verify HTML tags are balanced**

Run:

```bash
for t in div table tr td; do
  echo "$t open=$(grep -o "<$t[ >]" README.md | wc -l | tr -d ' ') close=$(grep -o "</$t>" README.md | wc -l | tr -d ' ')"
done
```

Expected: `open` equals `close` for every tag. (Markdown link syntax `[![...](...)](...)`  contains no HTML tags, so it does not affect these counts.)

- [ ] **Step 6: Verify the section order end to end**

Run:

```bash
grep -n '^### ' README.md
```

Expected, in this order: `👋 About me`, `🏆 Awards & Recognition`, `🎯 What I build best`, `🚀 Featured Projects`, `🧰 Tech I work with`.

- [ ] **Step 7: Verify all external links resolve**

Run:

```bash
for u in "https://www.linkedin.com/in/rodrigoscharp/" \
         "https://instagram.com/rodrigoscharp" \
         "https://github.com/rodrigoscharp/WalletCore" \
         "https://github.com/rodrigoscharp/Athena-Matching-Engine" \
         "https://github.com/rodrigoscharp/BETO-IA" \
         "https://github.com/rodrigoscharp/HelpNote_-IA" ; do
  printf '%-60s %s\n' "$u" "$(curl -s -o /dev/null -w '%{http_code}' -L "$u")"
done
```

Expected: `200` for each. A `404` on a GitHub URL means the repo name is wrong or the repo is private — report it rather than silently changing the link. LinkedIn and Instagram may return `999` or `4xx` to non-browser clients even when the profile is live; treat a non-200 on those two as "check manually in a browser", not as a failure.

- [ ] **Step 8: Visual render check**

Push the branch and open `https://github.com/rodrigoscharp` (or the file view on the branch) in a browser. Confirm by eye:

- The typing SVG animates through all five lines, including `2× National Award Winner`.
- The four social badges sit on one centered row.
- The Awards table renders as two side-by-side cells, not stacked or collapsed.
- The Featured Projects table renders with four rows and no broken pipes.
- The skillicons row shows six icons including AWS.
- Everything is legible in **both** GitHub light and dark themes — switch themes and re-check.

- [ ] **Step 9: Commit any fixes**

If Steps 1–8 required no edits, skip this step. Otherwise:

```bash
git add README.md
git commit -m "Fix README verification issues

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage:**

| Spec section | Task |
|:---|:---|
| Structure (7 sections, awards third) | Tasks 1–7; order asserted in 3.3, 5.4, 8.6 |
| 1. Header + badges | Task 1 |
| 2. About | Task 2 |
| 3. Awards & Recognition | Task 3 |
| 4. What I build best | Task 4 |
| 5. Featured Projects | Task 5 |
| 6. Tech I work with (+ AWS) | Task 6 |
| 7. CTA | Task 7 |
| Non-goal: no stats widgets | No task adds them; nothing in the current file to remove |
| Non-goal: no timeline, no education | No task adds them |
| Decision: Athena metric | Task 4 Step 3; Task 8 Step 1 |
| Decision: drop LMAX / event sourcing / CQRS | Task 4 Step 2; Task 8 Step 1 |
| Constraint: alt on every `<img>` | Task 8 Step 4 |
| Constraint: no title as headline | Task 2 Step 3; Task 8 Step 3 |
| Verification items 1–6 | Task 8 Steps 1–8 |

No gaps.

**Placeholder scan:** No TBD/TODO, no "similar to Task N", no "add appropriate handling". Every step contains the literal content to write or the literal command to run.

**Consistency check:** Heading text is `### 🎯 What I build best` in Task 4 and in the Task 8 Step 6 expected order — consistent. The Athena metric string `100k+ orders/s, sub-100µs p99` is byte-identical in Global Constraints, Task 4, Task 5, and Task 8 Step 2. The `HelpNote_-IA` repo slug is identical in Task 5 Steps 1, 2, and Task 8 Step 7. Task 3 Step 4 expects `open=2 close=2` for `<table>`, which holds because the only tables at that point are the Awards table and the pre-existing tech-stack table — the Featured Projects table (Task 5) is Markdown, not HTML, so it never affects tag counts.
