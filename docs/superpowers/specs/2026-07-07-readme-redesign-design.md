# README Redesign — Design

## Contexto

O README do perfil (`rodrigoscharp/rodrigoscharp`) está com visual fraco e desatualizado:

- A seção **Featured Projects** lista só 2 projetos (Athena Matching Engine, Own-Jarvis), deixando de fora trabalho recente relevante.
- O link para **Own-Jarvis** aponta para um repositório que foi renomeado para `BETO-IA` (o link ainda funciona via redirect do GitHub, mas não é a URL canônica).
- Os widgets de **Stats** (`github-readme-stats.vercel.app`) dependem de uma instância pública compartilhada que está retornando `503` de forma intermitente — causa provável dos ícones de "imagem indisponível" observados pelo usuário.
- O snake animation (`github-snake.svg`) e o typing SVG do header funcionam normalmente (são gerados via GitHub Action self-hosted ou serviço estável).

## Objetivo

Redesenhar o README para:
1. Ter mais impacto visual, mantendo (e expandindo) a linha de widgets/animações já existente.
2. Mostrar 5 projetos em destaque em vez de 2, com descrições e badges melhores.
3. Corrigir o link quebrado/desatualizado do BETO-IA.
4. Não introduzir novas dependências de infraestrutura (sem self-host de novos serviços) — a instabilidade ocasional dos Stats é aceita como está.

## Estrutura final

```
Header (typing SVG + badges de contato)
→ Sobre (parágrafo atualizado)
→ Stack (inalterado)
→ Featured Projects (5 cards)
→ Stats (inalterado)
→ Footer/Contato (inalterado)
```

## Seção "Sobre"

Substituir o parágrafo atual por:

> Software engineer from Brazil. I build production systems across fintech, banking and AI — from a matching engine processing **>100k orders/s** to a digital wallet with double-entry ledger and an AI assistant that runs entirely on your own server. My core stack is **Java + Spring Boot**; I also ship full-stack when the job calls for it.

Mudança-chave em relação ao original: "Backend engineer" → "Software engineer" (reflete o escopo full-stack + fintech/banking/AI mais amplo trazido pelos novos projetos).

Idioma do README permanece **inglês** (conversa de design foi em português, mas o conteúdo publicado mantém o idioma original do repositório).

## Featured Projects

Ordem final dos 5 cards: **Athena Matching Engine → WalletCore → BETO-IA → HelpNote-IA → internet-banking-java**.

Formato de cada card: título linkado, linha de badges (ícones [skillicons.dev](https://skillicons.dev) para tecnologias suportadas + badges customizados shields.io para as que não têm ícone — mesmo padrão já usado na seção Stack para Groq/ElevenLabs), parágrafo de descrição com métricas em negrito quando existirem, link de demo quando disponível.

**gRPC** e **JWT** não são suportados pelo skillicons.dev (validado via teste manual) — usar badge de texto shields.io para esses dois.

### 1. Athena Matching Engine
- Link: `https://github.com/rodrigoscharp/Athena-Matching-Engine`
- Badges: skillicons `java,spring,kafka,redis,postgres,docker` + badge `gRPC`
- Descrição (mantida do README atual): "High-performance order matching engine for financial trading. Single-writer design using LMAX Disruptor achieves **>100k orders/s** throughput with **<10µs p50 latency**. Event sourcing + CQRS, hexagonal architecture, multi-protocol (REST, gRPC, WebSocket), full observability with Grafana dashboards."

### 2. WalletCore (novo)
- Link: `https://github.com/rodrigoscharp/WalletCore`
- Badges: skillicons `java,spring,postgres,redis,docker` + badges `RabbitMQ`, `JWT`
- Descrição: "Production-grade digital wallet REST API. Atomic transfers with double-entry ledger and pessimistic locking, JWT auth with rotating refresh tokens, exponential retry + dead-letter queue for resilience, idempotency keys, rate limiting, and Testcontainers-based integration tests (real Postgres + RabbitMQ, no mocks)."

### 3. BETO-IA (renomeado de "Own-Jarvis")
- Link corrigido para: `https://github.com/rodrigoscharp/BETO-IA` (nome do repo atual; o antigo `Own-Jarvis` foi renomeado)
- Nome de exibição: **BETO-IA**
- Badges: skillicons `nextjs,ts,react,vercel,supabase` + badges `Groq`, `ElevenLabs`
- Descrição (mantida do README atual): "Privacy-first voice and text assistant that runs on your own server — no subscriptions, no data collection. Voice-activated with keyword detection, integrates with Spotify, Google Calendar, Gmail and GitHub. Powered by Groq LLaMA 3.1 with ElevenLabs TTS and a 3D animated particle orb interface."

### 4. HelpNote-IA (novo)
- Link: `https://github.com/rodrigoscharp/HelpNote_-IA`
- Demo: `https://help-note-ia.vercel.app`
- Badges: skillicons `js,java,html,css`
- Descrição: "AI-powered note-taking assistant for lectures and technical talks. Transcribes audio, extracts keywords, classifies topics, and auto-generates complementary explanations to turn raw notes into structured, reviewable content."

### 5. internet-banking-java (novo)
- Link: `https://github.com/rodrigoscharp/internet-banking-java`
- Badges: skillicons `java,spring,mysql,html,css,js`
- Descrição: "Internet banking REST API with Spring Security-based authentication, JPA persistence and validation layer — core account and transaction operations over a relational MySQL backend."

## Stats

Mantido como está hoje (github-readme-stats, streak-stats, snake animation). A instância pública do `github-readme-stats.vercel.app` é conhecida por instabilidade ocasional (retornou 503 durante a análise deste design); decisão explícita do usuário foi **não** investir em self-host ou provedor alternativo agora — aceitar o comportamento intermitente.

## Fora de escopo

- Seção "Building Now" / atualmente trabalhando — descartada explicitamente.
- Self-host de widgets de Stats — descartado explicitamente.
- Redução do número de projetos em destaque (top 3-4 + lista compacta) — descartada, os 5 ficam com o mesmo formato de card.
- MunoApp, Location-APP, Sistema-de-Treino-particular, Jusol-LP, Rocketseat-estudos — não entram nesta rodada.

## Verificação

Depois de implementado:
- Renderizar o README localmente (preview Markdown) e conferir que todas as imagens/badges carregam (skillicons, shields.io, typing SVG, snake, stats).
- Conferir que os 5 links de projeto e o link de demo do HelpNote-IA resolvem (200 ou redirect esperado).
- Conferir visualmente em tema claro e escuro do GitHub (os SVGs/badges atuais já são dark-theme-first; confirmar que não há elemento ilegível no tema claro).
