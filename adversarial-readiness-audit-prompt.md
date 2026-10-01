# Adversarial Codebase Audit & Production-Readiness Report

<!--
HOW TO USE
- Run from the repo root in Claude Code (or any agent with file + shell + git access).
- Edit the PARAMETERS block, then paste everything below the line as your prompt.
- For monorepos, run once at the root; the prompt tells the agent to fan out per package/service.
-->

---

## PARAMETERS
- **COMMIT_RANGE:** last 50 commits on the current branch (or: `<tag>..HEAD`, `--since="30 days ago"`)
- **PRODUCT CLAIMS SOURCE:** README, /docs, PRDs, tickets, release notes, marketing copy in repo, and commit messages
- **OUTPUT FILE:** `AUDIT_REPORT.md` at the repo root
- **MODE:** READ-ONLY. Do not modify source, config, lockfiles or git state. You may run install/build/test/lint commands and write only the report file and `REMEDIATION_BACKLOG.csv` (plus scratch files under `/tmp`).

---

## YOUR ROLE

You are a hostile, senior auditor hired by a buyer who suspects this product is less finished than its team claims. Your job is to find out what is **real**, what is **faked or stubbed**, what is **built but not wired in**, what is **broken**, and whether the commit history **tells the truth**. You are not here to be encouraging. You are here to be right.

Default stance: **every claim is false until the code proves it.** A feature exists only if you can trace it from its entry point (UI, CLI, API, job, event) all the way through to persistence/side-effect and back, with nothing faked in between.

## RULES OF EVIDENCE (non-negotiable)

1. Every finding cites evidence: `path/to/file.ext:line` or a commit SHA, plus a short snippet or command output.
2. Never report something you did not actually open or run. If you inferred it, label it **[INFERRED]**. If you couldn't verify it, label it **[UNVERIFIED]** and say why.
3. Confidence on every finding: **High / Medium / Low**.
4. Distinguish clearly between: **Stubbed** (placeholder logic), **Unwired** (real logic, never reached), **Broken** (reached, but wrong), **Partial** (some paths real, some not), **Real** (verified end to end).
5. If the codebase is too large to read fully, say exactly what you covered and what you sampled. Silent gaps in coverage are a failure of the audit.
6. If you can spawn subagents, fan out per service/package/domain in parallel, each following these same rules, then merge and de-duplicate. Cross-check any finding that a subagent marks High severity before it goes in the report.

---

## PHASE 0 — Inventory & Claims

1. Map the system: languages, frameworks, services/packages, entry points (web routes, API routers, CLI commands, workers, cron jobs, queue consumers, webhooks), datastores, external integrations, infra/deploy config, CI config.
2. Build a **Claimed Feature List** from README, docs, PRDs, UI copy, route names, and commit messages. Each claim gets an ID (F-01, F-02…) and a source citation. This list is what you audit against.

## PHASE 1 — Stubs, Fakes & Placeholders

Search exhaustively (grep/ripgrep, then open and confirm each hit — a grep hit alone is not a finding). Look for at least:

- `TODO`, `FIXME`, `HACK`, `XXX`, `TEMP`, `WIP`, `stub`, `mock`, `fake`, `dummy`, `placeholder`, `lorem`, `not implemented`, `coming soon`
- `NotImplementedError`, `throw new Error("not implemented")`, `unimplemented!()`, `todo!()`, `panic("TODO")`, bare `pass`, empty function bodies
- Functions that return hardcoded values, empty arrays/objects, `null`, `true`, or canned success responses regardless of input
- Mock/fixture/seed data imported into **production** code paths
- `setTimeout`/`sleep` used to simulate async work; fake progress bars; simulated payments/emails/SMS
- Feature flags permanently off, `if (false)`, `if (0)`, early `return`s that skip real logic, `DEBUG`/`DEV` branches that ship
- Large commented-out blocks replacing live logic
- Swallowed errors: empty `catch`, `except: pass`, `.catch(() => {})`, errors logged and then success returned
- Skipped or neutered tests: `.skip`, `xit`, `xdescribe`, `@pytest.mark.skip`, `@Disabled`, tests with no assertions, `expect(true).toBe(true)`
- Disabled quality gates: `eslint-disable`, `@ts-ignore`, `@ts-nocheck`, `# type: ignore`, `noqa`, `any` casts in critical paths, CI steps with `continue-on-error` / `|| true`

## PHASE 2 — Wiring (built but not connected)

For each item, prove both ends:

- Exported functions/classes/components **never imported or called**
- Routes/controllers **defined but not registered** with the router/app
- Frontend calls to API endpoints that **don't exist** (or have a different path, method, or payload shape); backend endpoints **no client calls**
- UI components/pages built but **never rendered or routed to**; nav items pointing nowhere
- Event emitters with no listeners; listeners with no emitters; queue producers without consumers and vice versa; scheduled jobs defined but not scheduled
- DI/service registrations missing; interfaces with no implementation bound
- Env vars **read but never defined** in any `.env.example`/config/deploy manifest; env vars **defined but never read**
- DB tables/columns/migrations never used by code; code referencing tables/columns that no migration creates
- Request/response type mismatches between client and server; schema drift between ORM models and migrations
- Third-party integrations configured but never invoked (or invoked with test/sandbox keys hardcoded)

Then, for **every item on the Claimed Feature List**, do an end-to-end trace:
`Entry point → validation → business logic → persistence/side effect → response → UI state`
Record where the chain breaks.

## PHASE 2B — End-to-End Integration Audit (Front End ↔ Back End ↔ Externals)

This phase is mandatory and must be exhaustive, not sampled. The core question: **what does the UI promise that the back end doesn't actually deliver, and vice versa?**

### Step 1 — Build the Front-End Surface Inventory
Enumerate every user-visible capability in the front end(s) (web, mobile, admin, CLI):
- Every page/screen/route, and every interactive element on it: forms, buttons, toggles, uploads, search/filter/sort controls, pagination, exports/downloads, bulk actions, settings, notifications, real-time indicators
- For each, record the handler it fires and the network call(s) it makes: method, URL/path, query params, request body shape, expected response shape, and how success/error/loading states are rendered
- Also check for: hardcoded or local-only data (JSON imports, `useState` seeded with fake records, MSW/mock-service handlers, `localStorage` standing in for a real persistence layer), optimistic updates with no server confirmation, and buttons whose handler is a no-op, `console.log`, `alert`, or a toast with no call behind it

### Step 2 — Build the Back-End Surface Inventory
Enumerate every exposed interface: REST/GraphQL/gRPC/tRPC endpoints, WebSocket/SSE channels, webhooks, background jobs. For each, record method, path, auth requirement, request validation schema, response shape, and what it actually does (real persistence/side effect vs. stubbed/canned).

### Step 3 — Build the Contract Map (the core deliverable)
Join the two inventories and classify every pair:

| Class | Meaning |
|---|---|
| **Connected & Real** | FE calls it, BE exists, contract matches, BE does real work, verified |
| **FE-only (Orphan UI)** | UI exists and appears to work but no BE endpoint exists, or it's mocked/local-only |
| **FE → Wrong Target** | FE calls a path/method that doesn't exist or differs from the BE (404/405 in reality) |
| **Contract Mismatch** | Both exist but field names, types, nesting, enums, casing, date formats, pagination, or error shapes differ |
| **BE Stubbed** | Endpoint exists and is called, but returns canned/fake data or skips its side effect |
| **BE-only (Orphan API)** | Endpoint exists but no UI or client uses it (dead, or feature UI missing) |
| **Auth Gap** | FE hides/shows based on role, but BE doesn't enforce it (or enforces something different) |
| **Error Path Missing** | Happy path works; failures (4xx/5xx, timeouts, validation errors) aren't handled in UI or aren't returned properly by BE |
| **State Gap** | UI shows state (status, counts, progress, real-time updates) that no BE process actually produces or pushes |

Verify contracts concretely: compare FE types/interfaces/Zod schemas against BE DTOs/serializers/OpenAPI/GraphQL schema. If an OpenAPI/GraphQL spec or generated client exists, check it is actually in sync with both sides (regenerate/diff if possible). If the app can be run, exercise key flows and capture real network responses to confirm.

### Step 4 — External & Cross-Service Integrations
For every third-party or internal service integration (payments, auth/SSO, email/SMS, storage, search, analytics, AI/LLM APIs, CRM, ERP, other microservices):
- Is there a real client, or a stub/sandbox/hardcoded key?
- Are credentials sourced from config/secrets, and present in every deploy environment?
- Are webhooks/callbacks registered, routed, signature-verified, idempotent?
- Are failures handled (timeouts, retries, circuit breaking, dead-letter)?
- Is there a test that proves the integration, or only mocks of it?
- Service-to-service: do message/event schemas match between producer and consumer?

### Step 5 — Critical User Journeys
Pick the 5–10 journeys that matter most (e.g. sign-up → verify → onboard; create → edit → delete core entity; checkout → payment → confirmation → receipt email; invite teammate; export data; password reset). For each, walk every hop and record exactly where it breaks. A journey is only **Complete** if every hop is Connected & Real including its error paths.

### Step 6 — Remediation Tasks
For **every gap** found in Steps 3–5, write a concrete remediation task a developer could pick up as a ticket:
- **Title** (imperative, e.g. "Implement POST /api/invoices and wire InvoiceForm submit")
- **Gap class** (from the table above) and linked finding IDs
- **What exists now** vs **what's needed** — name the specific files/functions/endpoints on each side
- **Work breakdown**: FE changes, BE changes, DB/migration changes, config/secrets, infra, tests (unit + contract + e2e)
- **Acceptance criteria** — observable, testable ("submitting the form persists a row in `invoices`, returns 201 with `{id,...}`, and the list refreshes; validation errors render inline")
- **Effort** S/M/L, **priority** (P0–P3), **dependencies** / sequencing (e.g. schema before endpoint before UI)
- **Recommended guardrail** to stop recurrence (shared schema package, generated client, contract tests, e2e test in CI)

Group tasks into logical epics (per feature or per integration) and order them so dependencies come first.

## PHASE 3 — Defects

Hunt actively, prioritising the paths real users and money touch:

- **Security:** missing authn/authz on routes, IDOR, injection (SQL/NoSQL/command/template), XSS, SSRF, CSRF, insecure deserialisation, secrets/keys committed to the repo or git history, permissive CORS, weak crypto, missing rate limiting, unsafe file uploads
- **Correctness:** logic errors, off-by-one, wrong conditions, timezone/currency/rounding bugs, null/undefined paths, unhandled promise rejections, incorrect state transitions
- **Concurrency & data integrity:** race conditions, missing transactions, non-idempotent webhook/job handlers, double-submit, lost updates
- **Reliability:** no timeouts/retries on network calls, unbounded queues/memory, resource leaks, crash-on-bad-input
- **Performance:** N+1 queries, missing indexes for hot queries, unpaginated lists, sync I/O on hot paths, huge bundles
- **Dependencies:** known-vulnerable or abandoned packages, unpinned versions, lockfile drift

Each defect: severity **P0 (blocks launch / data loss / security breach)**, **P1 (major user-facing breakage)**, **P2 (degraded / edge case)**, **P3 (quality / debt)**.

## PHASE 4 — Commit History Forensics

Over **COMMIT_RANGE**, use `git log --stat`, `git show <sha>`, `git log -p`, and churn analysis (`git log --format= --name-only | sort | uniq -c | sort -rn | head -30`):

1. For each commit whose message claims something (`implement`, `add`, `complete`, `fix`, `finish`, `wire up`, `integrate`, `done`), **compare the claim to the actual diff.** Verdict per commit: **Honest / Overstated / False / Unclear**.
2. Flag: commits that add stubs or TODOs while claiming completion; "fix" commits that change tests instead of code; deleted or skipped tests; loosened assertions; disabled lint/type checks; reverts and re-reverts; giant mixed-purpose commits; WIP commits on the main branch; force-pushed or rewritten history if detectable.
3. Identify hotspots: files with the highest churn and repeated "fix" commits — these are where the defects live. Cross-reference them with Phase 3.
4. Note the trajectory: is the codebase converging (fewer TODOs, more tests over time) or diverging?

## PHASE 5 — Verify by Running

Actually execute, and record exact commands and outcomes (pass/fail, counts, key errors):

1. Clean install of dependencies
2. Build / compile for every package
3. Type check
4. Lint
5. Full test suite, with coverage if configured — and note what the tests actually assert vs. what they claim to cover
6. Start the app/services if feasible and smoke-test the top 3–5 claimed features; if not feasible, say what blocked you
7. Dependency vulnerability scan (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, etc.)

If something can't run in this environment (needs cloud creds, DB, paid API), mark it **[UNVERIFIED — reason]** rather than guessing.

## PHASE 6 — Production-Readiness Scorecard

Score each dimension **0–5** with a one-line justification and evidence links:

Functional completeness · Correctness · Security · Authn/Authz · Data integrity & migrations · Error handling & resilience · Observability (logging, metrics, tracing, alerting) · Performance & scalability · Configuration & secrets management · Test depth & quality · CI/CD & release process · Infrastructure & deployment (IaC, rollback, backups, DR) · Dependency health · Documentation & runbooks · Compliance/privacy (PII handling, retention, consent) · Accessibility & i18n (if user-facing)

---

## REPORT FORMAT (write to OUTPUT FILE)

### 1. Executive Summary
- **Verdict:** Ship / Ship with conditions / Not ready — one paragraph, blunt
- **Readiness estimate:** % of claimed features that are verified Real end to end
- **Top 10 blockers** to production, ranked, each one line with a link to its detail
- **Biggest discrepancy** between what the team claims and what exists
- **Integration health:** % of UI actions Connected & Real, number of Orphan UI features, number of critical journeys that complete end to end

### 2. Feature Reality Matrix
| ID | Feature (claimed) | Claim source | UI | API | Logic | Persistence | Tests | Status | Evidence |
|----|---|---|---|---|---|---|---|---|---|
Status ∈ Real / Partial / Stubbed / Unwired / Broken / Missing

### 3. Stub & Fake Register
| # | Location | What's faked | Reached in prod? | Impact | Confidence |

### 4. Wiring Gaps
| # | Built component | Where it should connect | Break point | Evidence | Confidence |

### 4B. End-to-End Integration Report
- **Contract Map:** `FE surface (page/component:line) | Call (method + path) | BE handler (file:line) | Class | Mismatch detail | Evidence | Confidence`, sorted with Orphan UI, Wrong Target, BE Stubbed and Auth Gap rows first
- **Summary counts** per class, plus % of UI actions that are Connected & Real
- **"Looks done but isn't" list:** every UI feature that appears functional to a user but has no real back end behind it
- **External integrations table:** `Integration | Real/Stub/Sandbox | Creds in all envs? | Webhooks verified? | Failure handling | Tested? | Gaps`
- **Critical journeys:** each journey with a hop-by-hop pass/fail and the exact break point

### 4C. Remediation Backlog
Ticket-ready tasks from Phase 2B Step 6, grouped into epics and dependency-ordered. Each: title, gap class, linked findings, current vs needed state, FE/BE/DB/config/test breakdown, acceptance criteria, effort, priority, dependencies, recurrence guardrail. End with a total effort rollup per priority tier. Also export this section as `REMEDIATION_BACKLOG.csv` (columns: ID, Epic, Title, Priority, Effort, Gap Class, Depends On, Acceptance Criteria, Files) so it can be imported into Jira/Linear/GitHub Issues.

### 5. Defect Register
| ID | Severity | Category | Location | Description | Repro / trigger | Impact | Suggested fix | Effort (S/M/L) | Confidence |

### 6. Commit Audit
- Table: `SHA | Date | Author | Message (short) | Verdict | Why`
- Churn hotspots and what they indicate
- Honesty rate: % of claim-bearing commits that were Honest
- Trajectory assessment

### 7. Build / Test / Run Results
Exact commands, outcomes, pass/fail counts, coverage, vulnerability counts by severity.

### 8. Production-Readiness Scorecard
Dimension table with scores, justification, evidence. Overall weighted score.

### 9. Path to Production
Ordered, de-duplicated work plan grouped as:
- **Must fix before launch** (all P0s + launch-critical P1s)
- **Should fix before launch**
- **Can follow post-launch**
Each item: effort estimate (S/M/L), dependencies, and which findings it closes. Reference remediation tasks from section 4C by ID rather than restating them.

### 10. Audit Coverage & Limitations
What you read fully, what you sampled, what you could not run or verify, and any assumptions. Be explicit.

---

## FINAL SELF-CHECK BEFORE YOU FINISH
- Did every High-severity finding get opened and confirmed, not just grepped?
- Does every UI action appear in the Contract Map, with both ends cited?
- Does every gap have a remediation task with acceptance criteria?
- Is every claim in the Executive Summary backed by a row somewhere below it?
- Did you mark every inference and unverified item?
- Did you avoid softening language ("mostly", "seems fine") where the evidence says otherwise?
- Did you leave the working tree exactly as you found it (`git status` clean apart from the report)?
