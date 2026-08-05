# GitHub Profile README — CV Alignment & Awards Highlight

**Date:** 2026-08-05
**Status:** Approved design
**Scope:** Rewrite `README.md` at the repo root (GitHub profile README for `rodrigoscharp/rodrigoscharp`)

## Problem

The current README sells Rodrigo as a backend engineer who enjoys hard technical problems. His CV sells someone who **leads a technology department, founded a startup, and won two national awards**. The README omits every one of those facts.

Three concrete gaps:

1. **Missing career substance.** No mention of the Director of Technology and Innovation role at Prefeitura de Ubatuba (6+ production systems, 100,000+ citizens), the MUNO food-tech startup, the two national awards, 4+ years of experience, or 30+ backend systems at Bitwise.
2. **Contradictory metrics.** README claims Athena does `>100k orders/s at <10µs p50`; the CV claims `100,000+ orders/second` and `sub-100µs p99`. Both are public under his name.
3. **Unsupported technical claims.** README cites LMAX Disruptor, event sourcing, and CQRS. Rodrigo has confirmed he has not used any of the three.

## Goals

- Make the README consistent with the CV on every factual claim.
- Give the two national awards prominent placement — they are the rarest signal on the profile.
- Keep the primary identity **Software Engineer**, not manager. Leadership and founding appear as *scope of delivered work*, never as a job title in a headline position.
- Add the Instagram creator presence (`@rodrigoscharp` — programming, dev life, career) without displacing engineering focus.
- Target audience: **international recruiters**. README stays in English.

## Non-Goals

- No GitHub stats widgets (streak, top languages, contribution cards). They read as noise to senior recruiters, and a "top language: TypeScript" badge would contradict the Java positioning.
- No employment timeline. The README is not a résumé mirror; LinkedIn and the CV cover that.
- No education section. Covered by LinkedIn.
- No changes to the CV PDF. This spec covers `README.md` only.

## Decisions Made

| Decision | Choice | Rationale |
|:---|:---|:---|
| Audience | International recruiters | Drives English, metric rigor, impact-first ordering |
| Positioning | Engineer who also leads | User wants software-engineer identity preserved while awards get weight |
| Athena metrics | `100k+ orders/s, sub-100µs p99` | CV version; p99 is the more honest and more respected metric |
| Instagram weight | Badge + one line in About | Content is Portuguese-language; secondary signal for the target audience |
| LMAX / event sourcing / CQRS | **Removed** | Not actually used — indefensible in an interview |
| GitHub stats widgets | Excluded | Noise; contradicts Java positioning |

## Design

### Structure

```
1. Header (typing SVG) + social badges
2. About
3. 🏆 Awards & Recognition
4. What I build best
5. Featured Projects
6. Tech I work with
7. CTA
```

Awards sit third — above the projects — because a national award is the rarest credential on the profile and the user explicitly asked for it to be highlighted.

### 1. Header + badges

Keep the existing `readme-typing-svg` component: JetBrains Mono, weight 600, size 24, color `#58A6FF`, centered, width 640. Replace the rotating lines with:

```
Hey, I'm Rodrigo Scharp 👋
Software Engineer · Brazil
Java 21 + Spring Boot 3
Systems serving 100,000+ citizens
2× National Award Winner
```

Badges, `style=for-the-badge`, centered, in this order:

| Badge | Color | Target |
|:---|:---|:---|
| LinkedIn | `0A66C2` | `https://www.linkedin.com/in/rodrigoscharp/` |
| Email | `D14836` | `mailto:rodrigosharp99@gmail.com` |
| Instagram | `E4405F` | `https://instagram.com/rodrigoscharp` |
| GitHub | `181717` | `https://github.com/rodrigoscharp` |

### 2. About

Three paragraphs:

> Software engineer from Brazil with **4+ years** building production systems across government, fintech and food-tech. I lead the technology team at the **Ubatuba city government**, where we've shipped **6+ systems serving 100,000+ citizens** — work recognized with **two national awards**. I also founded **MUNO**, a food-tech startup, where I built the backend and cloud infrastructure end to end.
>
> My core stack is **Java 21 + Spring Boot 3**, and I go full-stack with **Next.js + TypeScript** when a product needs it. I care about the hard parts: correctness under concurrency, resilient architecture, and code that holds up in production rather than just in a demo.
>
> Outside of engineering, I create content on programming, dev life and career as **[@rodrigoscharp](https://instagram.com/rodrigoscharp)** on Instagram.

No job titles appear. Leadership is conveyed through delivered scope ("we've shipped 6+ systems serving 100,000+ citizens"), founding through what was built ("built the backend and cloud infrastructure end to end").

### 3. Awards & Recognition

Centered two-column table, one award per cell:

| 🏆 **Smart City Award** | 🏆 **Cidade Inovadora Award** |
|:---|:---|
| National recognition for digital transformation and smart city initiatives at Prefeitura de Ubatuba. | National recognition for innovation in public administration and technology-driven municipal governance. |

Award names stay in their original form (`Cidade Inovadora` is not translated — it is the award's actual name).

### 4. What I build best

Six bullets, each `**Label** — detail`:

- **Systems at public scale** — 6+ government systems in production, serving 100,000+ citizens
- **Financial engineering** — double-entry ledgers, order matching (**100k+ orders/s, sub-100µs p99**), atomic transfers with pessimistic locking, idempotency
- **Distributed architecture** — REST · gRPC · WebSocket, event-driven with RabbitMQ and Kafka, clean architecture
- **Resilience & reliability** — retries with backoff, dead-letter queues, rate limiting, Testcontainers integration tests
- **AI & LLM integration** — voice/text assistants with Groq LLaMA + ElevenLabs, self-hosted and privacy-first
- **Cloud & DevOps** — AWS (ECS, ALB, CloudFront, API Gateway, Lambda), Docker, CI/CD

Every claim here traces to a line in the CV. LMAX Disruptor, event sourcing, CQRS, single-writer designs, and Grafana/observability-from-day-one are dropped — none appear in the CV, and the first three were confirmed as not used.

### 5. Featured Projects

Four-row table. Project names link to their repos.

| Project | What it is | Stack |
|:---|:---|:---|
| **WalletCore** | Digital wallet API — double-entry ledger, JWT auth, pessimistic locking, async notifications | Java 21 · Spring Boot 3 · PostgreSQL · RabbitMQ · Redis |
| **Athena Matching Engine** | Order matching engine — 100k+ orders/s, sub-100µs p99, lock-free design | Java 21 · Spring Boot · Kafka · Redis · gRPC |
| **BETO IA** | Self-hosted voice AI assistant — Spotify, Google Calendar and GitHub integrations, no third-party subscriptions | Next.js 14 · TypeScript · Groq · ElevenLabs · Supabase |
| **HelpNote IA** | Transcribes lecture and event audio, extracts keywords, generates enriched summaries | Java · Spring Boot · PostgreSQL · LLM |

Repo URLs, from the CV:

- `https://github.com/rodrigoscharp/WalletCore`
- `https://github.com/rodrigoscharp/Athena-Matching-Engine`
- `https://github.com/rodrigoscharp/BETO-IA`
- `https://github.com/rodrigoscharp/HelpNote_-IA`

This replaces the current "📌 My featured work is pinned below" line — a recruiter should not have to scroll and interpret pins.

### 6. Tech I work with

Keep the existing centered `skillicons.dev` table, four rows, `theme=dark`. One change: add `aws` to the Data & Infra row.

| Row | Icons |
|:---|:---|
| Backend | `java,spring,nodejs` |
| Full-stack | `nextjs,ts,react` |
| Data & Infra | `postgres,mysql,redis,kafka,docker,aws` |
| AI & LLM | Groq · LLaMA 3.1 · OpenAI · ElevenLabs (shields.io `flat-square` badges, unchanged) |

RabbitMQ has no skillicons entry; it is already covered in the "What I build best" bullets.

### 7. CTA

Centered, closing the file. Two `for-the-badge` badges side by side:

- `Let's connect` → LinkedIn (`0A66C2`)
- `Follow my content` → Instagram (`E4405F`)

## Constraints

- **Single file.** All changes land in `README.md`. No new files, no workflows, no scripts.
- **GitHub-flavored Markdown only.** Rendered by GitHub's profile README renderer: no raw CSS, no `<style>`, no JavaScript. Centering is done with `<div align="center">` and HTML tables, matching the existing file.
- **External services** already in use and retained: `readme-typing-svg.demolab.com`, `img.shields.io`, `skillicons.dev`.
- **Alt text** required on every `<img>`, as in the current file.

## Verification

The README is a static document; verification is a checklist, not a test suite.

1. **Factual consistency** — every number and claim in the README appears in the CV: 4+ years, 6+ systems, 100,000+ citizens, 2 national awards, 100k+ orders/s, sub-100µs p99.
2. **No unsupported claims** — `grep -iE 'disruptor|event sourcing|cqrs|single-writer|grafana|10µs|p50'` returns nothing.
3. **Links resolve** — LinkedIn, Instagram, mailto, and all four project repos return 200.
4. **Images render** — typing SVG, all shields.io badges, and all skillicons images load; every `<img>` has an `alt` attribute.
5. **Visual check** — render the file on GitHub and confirm centering, table layout, and badge alignment in both light and dark themes.
6. **Title/identity check** — no job title ("Director", "CTO", "Founder") appears as a headline or heading; each is either absent or embedded in prose describing delivered work.

## Open Questions

None.
