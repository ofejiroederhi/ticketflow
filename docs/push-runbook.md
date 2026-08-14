# Push Runbook, Step by Step

Companion to [`push-plan.md`](push-plan.md), which explains *why*. This one is *what to type*.

**Read this first.** Only M3's laptop has the code. Everyone else clones an empty repository,
so the order below is not optional: Phase A and B must finish before anyone else can do
anything. After that, the four sprints run with everyone working in parallel.

**Names used below**

| | Member | GitHub / git email | Owns |
|---|---|---|---|
| M1 | Ijeoma | `ijeomac@uni.coventry.ac.uk` | DevOps, CI, containers |
| M2 | Abiola | `abiolao5@uni.coventry.ac.uk` | QA, tests, quality docs |
| M3 | Ederhi | `ederhio@uni.coventry.ac.uk` | Backend |
| M4 | Adetunji | `adetunjim@uni.coventry.ac.uk` | Frontend |
| M5 | Akoki | `akokic@uni.coventry.ac.uk` | Data and ML |

**Remote:** `git@github.com:ofejiroederhi/ticketflow.git`

That is an **SSH** URL, so each member needs an SSH key on their GitHub account
(*Settings, SSH and GPG keys*). Anyone who has not set one up can use the HTTPS form instead,
`https://github.com/ofejiroederhi/ticketflow.git`, and authenticate with a personal access
token when git asks. Both point at the same repository and can be mixed freely across the
team. Check which you have with `git remote -v`.

---

## Phase A. M1 only, once. Create the repository skeleton

**A1.** On GitHub, create the repository. **Do not** tick "Add a README", "Add .gitignore" or
"Choose a license". An empty repository is required, or step A5 will reject the push.

**A2.** M3 sends M1 two files by any means (Teams, email): `.gitignore` and `README.md`. These
are the only files that must exist before the first commit.

**A3.** M1, on their own laptop:

```bash
mkdir ticketflow && cd ticketflow && git init -b main
```

**A4.** Set identity for this repository only:

```bash
git config user.name "Ijeoma" && git config user.email "ijeomac@uni.coventry.ac.uk"
```

**A5.** Add the two files, commit, push:

```bash
git add .gitignore README.md
git commit -m "chore: repository scaffold and ignore rules"
git remote add origin git@github.com:ofejiroederhi/ticketflow.git
git push -u origin main
```

**A6.** Create the integration branch:

```bash
git checkout -b dev && git push -u origin dev
```

**A7.** On GitHub: **Settings, Collaborators**, add the other four with **Write** access.

**A8.** On GitHub: **Settings, Branches, Add branch protection rule** for `main`. Tick
*Require a pull request before merging* and set *Required approvals* to **1**.

> Do **not** protect `dev`. Protecting both means every commit needs someone else awake,
> and the team stops moving.

**A9.** Tell the team the repository is ready.

---

## Phase B. M3 only, once. Get the code into the repository

**B1.** M3, in the existing working folder `~/Projects/ticketflow`:

```bash
git remote add origin git@github.com:ofejiroederhi/ticketflow.git
git fetch origin
```

**B2.** Set identity:

```bash
git config user.name "Ederhi" && git config user.email "ederhio@uni.coventry.ac.uk"
```

**B3.** Confirm the two report PDFs and the `.docx` will not be pushed:

```bash
git check-ignore "docs/report/sample report.pdf" "docs/report/Assessment Brief.pdf" && echo "IGNORED, good"
```

If that prints nothing, stop. The `.gitignore` did not travel. Fix it before continuing.

**B4.** Create the staging branch that nobody ever merges:

```bash
git checkout -b import/full-tree
git add -A
git commit -m "chore: import working tree (staging only, never merged)"
git push -u origin import/full-tree
```

**B5.** Confirm what landed:

```bash
git ls-files | wc -l          # expect ~544
git count-objects -vH | grep size-pack   # expect well under 50 MB
```

**B6.** Tell the team `import/full-tree` is available.

---

## Phase C. Everyone, once. Set up your laptop

Every member except M3 does this. **M3 skips to Phase D.**

**C1.**

```bash
git clone git@github.com:ofejiroederhi/ticketflow.git ticketflow && cd ticketflow
```

**C2.** Set your identity, per repository, using your own name and email from the table:

```bash
git config user.name "Adetunji" && git config user.email "adetunjim@uni.coventry.ac.uk"
```

**C3.** Verify it took. This is the single most important check in the whole runbook:

```bash
git config user.email
```

If that shows anything other than your own university address, fix it now. Commits made with
the wrong email are attributed to the wrong person and cannot be corrected without rewriting
history.

**C4.** Fetch the staging branch so you can take files from it:

```bash
git fetch origin import/full-tree
```

---

## Phase D. The four sprints

The loop is identical every sprint. Only the paths change. **Every member's exact commands are
written out below**, so nothing has to be assembled by hand.

### The loop, in general

```bash
# 1. Start from the latest dev
git checkout dev && git pull origin dev

# 2. Branch for this sprint's work
git checkout -b feat/<area>-s<N>

# 3. Take your paths out of the staging branch
git checkout origin/import/full-tree -- <your paths for this sprint>

# 4. Commit, in two or three steps rather than one
git commit -m "feat(<area>): <what it does>"

# 5. Push
git push -u origin feat/<area>-s<N>
```

Then open a pull request into `dev` on GitHub, ask the member named in the `Pair-` tag to
approve it, merge, and delete the branch.

> **Name files, never directories**, unless the table says a directory. `git checkout <ref> --
> backend/src/presentation` takes all nineteen files under it, not the three that sprint wants.
> Check with `git status --short` before every commit: if the count is larger than the table,
> you named a directory.

### Commit message convention

```
<type>(<scope>): <what changed, imperative, under ~65 characters>

- <one decision or behaviour per bullet>
- <why it is this way, not what the diff already shows>
- <wrap at 72 columns; two to five bullets is the useful range>
```

`type` is one of `feat`, `fix`, `test`, `docs`, `chore`, `refactor`. `scope` is the area:
`auth`, `events`, `admission`, `checkout`, `concierge`, `ci` and so on.

**The bullets are where the marks are.** A subject line records what happened; the bullets
record the reasoning, and that is what `git log` is being read for in an assessed submission.
Each bullet should say something a reader could not work out from the diff. Never restate the
file list, which git already shows.

---

### Sprint 1, foundation, accounts and access control

Tag at the end: `v0.1.0-sprint1`

| Who | Branch | Paths to take |
|---|---|---|
| M1 | `feat/devops-s1` | `.github/ backend/Dockerfile frontend/Dockerfile docker-compose.yml backend/.dockerignore frontend/.dockerignore backend/.env.docker.example` |
| M3 | `feat/backend-s1` | `backend/package.json backend/package-lock.json backend/server.js backend/app.js backend/src/models/userModel.js backend/src/services/authService.js backend/src/services/userService.js backend/src/repositories/userRepository.js backend/src/presentation/controllers/authController.js backend/src/presentation/controllers/userController.js backend/src/presentation/routes/userRoutes.js backend/src/shared/ backend/eslint.config.js backend/.gitignore backend/.nvmrc backend/.prettierrc backend/LICENSE backend/README.md backend/views/` |
| M4 | `feat/frontend-s1` | `frontend/package.json frontend/package-lock.json frontend/next.config.ts frontend/tsconfig.json frontend/src/middleware.ts frontend/src/app/layout.tsx frontend/src/app/'(authentication)' frontend/src/app/my-profile/settings frontend/src/types frontend/src/styles frontend/src/providers frontend/public frontend/.eslintrc.json frontend/.gitignore frontend/README.md frontend/postcss.config.js frontend/src/app/error.tsx frontend/src/app/not-found.tsx frontend/src/app/icon.jpg frontend/src/app/manifest.ts frontend/src/app/robots.ts frontend/src/app/sitemap.ts` |
| M2 | `feat/qa-s1` | `backend/tests/unit/role.authz.test.js backend/tests/unit/models.test.js backend/tests/helpers frontend/vitest.config.mts frontend/vitest.setup.tsx frontend/playwright.config.ts` |
| M5 | `feat/dataml-s1` | nothing this sprint. M5's first code lands in Sprint 3. |

#### Exact commands, Sprint 1

**M1, DevOps**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/devops-s1

git checkout origin/import/full-tree -- .github/ backend/Dockerfile frontend/Dockerfile docker-compose.yml backend/.dockerignore frontend/.dockerignore backend/.env.docker.example
git commit -m "chore(ci): GitHub Actions pipeline and container stack

- Backend lint and tests, frontend typecheck, lint and component tests,
  on every push and pull request
- MongoDB starts as a single-node replica set, because booking and
  admission use transactions and a standalone mongod rejects them
- The replica set advertises 127.0.0.1 explicitly; with the container own
  hostname the driver resolves an address the runner cannot reach"

git push -u origin feat/devops-s1
```

**M3, backend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/backend-s1

git checkout origin/import/full-tree -- backend/package.json backend/package-lock.json backend/.gitignore backend/.nvmrc backend/.prettierrc backend/LICENSE backend/README.md backend/eslint.config.js
git commit -m "chore(backend): project scaffold and tooling

- Express application skeleton with lint and formatter configuration
- Node version pinned, so every laptop and CI runner agree"

git checkout origin/import/full-tree -- backend/src/models/userModel.js backend/src/shared/ backend/views/
git commit -m "feat(backend): user model and shared layer

- Four-role user schema: user, creator, usher and admin
- isRootAdmin is select:false, so it never reaches a client by accident
- Shared layer covers error types, the email transport and its Pug
  templates, QR generation and the JWT helpers"

git checkout origin/import/full-tree -- backend/src/services/authService.js backend/src/services/userService.js backend/src/repositories/userRepository.js
git commit -m "feat(auth): registration, login and password reset

- JWT issued in an HTTP-only cookie, so it is not readable by scripts
- Reset tokens stored hashed, expire in ten minutes, single-use
- Submitted role filtered through a frozen whitelist: only user and
  creator are self-assignable
- Closes a real privilege-escalation hole, not a hypothetical one. Any
  visitor could previously register as an administrator"

git checkout origin/import/full-tree -- backend/src/presentation/controllers/authController.js backend/src/presentation/controllers/userController.js backend/src/presentation/routes/userRoutes.js backend/server.js backend/app.js
git commit -m "feat(api): account routes and security middleware

- helmet, CORS with credentials, rate limiting, mongo-sanitize, xss and
  hpp all run ahead of the router
- Raw request body captured, so the payment webhook can verify its HMAC
  signature later
- Authorisation lives in the services, not here. Controllers never touch
  models; services never touch req or res"

git push -u origin feat/backend-s1
```

**M4, frontend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/frontend-s1

git checkout origin/import/full-tree -- frontend/package.json frontend/package-lock.json frontend/next.config.ts frontend/tsconfig.json frontend/postcss.config.js frontend/.eslintrc.json frontend/.gitignore frontend/README.md frontend/src/types frontend/src/styles
git commit -m "chore(frontend): Next.js scaffold, tooling and design tokens

- App Router with TypeScript and Tailwind
- Ambient type declarations are committed rather than generated, because
  CI typechecks without running a build and would otherwise fail on every
  image import"

git checkout origin/import/full-tree -- frontend/src/app/layout.tsx frontend/src/providers frontend/public frontend/src/app/error.tsx frontend/src/app/not-found.tsx frontend/src/app/icon.jpg frontend/src/app/manifest.ts frontend/src/app/robots.ts frontend/src/app/sitemap.ts
git commit -m "feat(frontend): application shell, providers and static assets

- Root layout, error and not-found boundaries, manifest, robots, sitemap
- TanStack Query and Zustand providers mounted once at the root"

git checkout origin/import/full-tree -- frontend/src/middleware.ts frontend/src/app/'(authentication)' frontend/src/app/my-profile/settings
git commit -m "feat(auth): sign-up, log-in, password reset and profile settings

- middleware.ts decodes the JWT cookie and redirects on expiry
- It is a UX guard only: no signature check, no role read. Every real
  authorisation decision stays server-side"

git push -u origin feat/frontend-s1
```

**M2, QA**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/qa-s1

git checkout origin/import/full-tree -- backend/tests/helpers frontend/vitest.config.mts frontend/vitest.setup.tsx frontend/playwright.config.ts
git commit -m "chore(test): test harnesses for both packages

- Shared database helper for integration tests
- Vitest with React Testing Library for components, Playwright for
  end-to-end journeys"

git checkout origin/import/full-tree -- backend/tests/unit/role.authz.test.js backend/tests/unit/models.test.js
git commit -m "test(auth): role decision and model unit tests

- Covers canChangeRole and canDeleteUser across every role pair
- Includes the cases that must fail: self-promotion, demoting the root
  admin, and a non-root admin granting admin
- Written against pure functions, so they run without a database"

git push -u origin feat/qa-s1
```

**M5** has no code this sprint. The Data and ML work begins in Sprint 3.

**Sprint 1 review.** M1 is Scrum Master. Once all four PRs are merged into `dev`:

```bash
git checkout main && git pull origin main
git merge --no-ff dev -m "Sprint 1: accounts, roles, profiles, CI and containers"
git tag -a v0.1.0-sprint1 -m "Sprint 1 increment"
git push origin main --tags
```

---

### Sprint 2, event creation and management

Tag: `v0.2.0-sprint2`. **M2 is Scrum Master and runs the merge.**

| Who | Branch | Paths to take |
|---|---|---|
| M3 | `feat/backend-s2` | `backend/src/models/eventModel.js backend/src/services/eventService.js backend/src/repositories/eventRepository.js backend/src/presentation/controllers/eventController.js backend/src/presentation/routes/eventRoutes.js` |
| M4 | `feat/frontend-s2` | `frontend/src/app/'(events)'/layout.tsx frontend/src/app/'(events)'/create-event frontend/src/app/'(events)'/edit-event frontend/src/app/'(events)'/my-events frontend/src/components frontend/src/assets frontend/src/utils frontend/src/hooks frontend/src/store` |
| M2 | `feat/qa-s2` | `backend/tests/unit/eventLiveness.test.js backend/tests/unit/pricing.test.js` |
| M1 | `feat/devops-s2` | `backend/scripts/` |

#### Exact commands, Sprint 2

**M3, backend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/backend-s2

git checkout origin/import/full-tree -- backend/src/models/eventModel.js backend/src/repositories/eventRepository.js
git commit -m "feat(events): event schema with tiers, access modes and currency

- Embedded ticket tiers, venue capacity, venue detail and structured
  location on one document
- accessMode is a first-class field, not a flag: public, invite_only and
  hybrid each change what the rest of the system permits
- An invite-only event carrying tiers is rejected, since it admits from
  the guest list only
- Currency is limited to what the payment provider can settle, which is
  why GBP and EUR are absent"

git checkout origin/import/full-tree -- backend/src/services/eventService.js
git commit -m "feat(events): event service with ownership enforcement

- Only the event creator or an admin may update or archive an event
- Enforced in the service, not the route, so the rule holds no matter
  which endpoint reaches it
- Archival is a soft delete: bookings, guests, chat and audit rows all
  survive, because the audit trail is what a door dispute needs"

git checkout origin/import/full-tree -- backend/src/presentation/controllers/eventController.js backend/src/presentation/routes/eventRoutes.js
git commit -m "feat(events): event API endpoints

- Public discovery routes sit ahead of the protect middleware; every
  organiser route sits behind it
- Multi-segment paths are registered before the single-segment /:slug
  route, or that route swallows them"

git push -u origin feat/backend-s2
```

**M4, frontend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/frontend-s2

git checkout origin/import/full-tree -- frontend/src/components frontend/src/assets frontend/src/utils frontend/src/hooks frontend/src/store
git commit -m "feat(ui): shared component library and client state

- Buttons, inputs, modals, cards and the navigation shell
- TanStack Query for server state, Zustand for local state
- Server actions read the JWT from the httpOnly cookie, so the token is
  never exposed to client-side JavaScript"

git checkout origin/import/full-tree -- frontend/src/app/'(events)'/layout.tsx frontend/src/app/'(events)'/create-event frontend/src/app/'(events)'/edit-event
git commit -m "feat(events): create and edit event forms

- Multi-section form with cover-image upload and preview
- Edit form pre-populated from the existing event
- Changing a tier price does not alter tickets already sold: their price
  was stamped at purchase"

git checkout origin/import/full-tree -- frontend/src/app/'(events)'/my-events
git commit -m "feat(events): My Events management surface

- Event cards with the per-event management links
- Guest list is offered only for invite-only and hybrid events, because a
  public event has no guest list and the API rejects the call"

git push -u origin feat/frontend-s2
```

**M2, QA**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/qa-s2

git checkout origin/import/full-tree -- backend/tests/unit/eventLiveness.test.js backend/tests/unit/pricing.test.js
git commit -m "test(events): liveness window and pricing arithmetic

- Pins the liveness rule, including the case that was wrong: an event
  whose start and end fall on the same day was never live, because the
  window closed at midnight rather than end of day
- Pricing tests assert the fee is computed in minor units and rounded
  down, so rounding never favours the platform by accident"

git push -u origin feat/qa-s2
```

**M1, DevOps**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/devops-s2

git checkout origin/import/full-tree -- backend/scripts/
git commit -m "chore(scripts): seeding, retention and load-test tooling

- Admin seeding runs from the CLI, so the first administrator has no
  in-application origin and cannot be created by signing up
- Retention sweep is a scheduled job rather than a request path, since it
  touches many records and must not block a user"

git push -u origin feat/devops-s2
```

**Sprint 2 review.** M2 is Scrum Master:

```bash
git checkout main && git pull origin main
git merge --no-ff dev -m "Sprint 2: event creation, tiers, currency and access modes"
git tag -a v0.2.0-sprint2 -m "Sprint 2 increment"
git push origin main --tags
```

---

### Sprint 3, discovery, guests, door operations and engagement

Tag: `v0.3.0-sprint3`. **M3 is Scrum Master.** The largest sprint, 132 points.

| Who | Branch | Paths to take |
|---|---|---|
| M3 | `feat/backend-s3` | `backend/src/models/guestModel.js backend/src/models/auditLogModel.js backend/src/models/messageModel.js backend/src/services/guestService.js backend/src/services/admissionService.js backend/src/services/usherService.js backend/src/services/networkingService.js backend/src/services/networkingGuestService.js backend/src/services/networkingNotificationService.js backend/src/services/retentionService.js backend/src/repositories/guestRepository.js backend/src/repositories/auditLogRepository.js backend/src/repositories/messageRepository.js backend/src/presentation/controllers/admissionController.js backend/src/presentation/controllers/guestController.js backend/src/presentation/controllers/usherController.js backend/src/presentation/controllers/networkingController.js` |
| M5 | `feat/dataml-s3` | `backend/src/services/chatbot backend/src/services/nlQuery backend/src/services/nlGuestQueryService.js backend/src/services/weatherService.js backend/src/presentation/controllers/chatController.js backend/src/presentation/controllers/nlQueryController.js backend/src/presentation/routes/chatRoutes.js backend/src/assets` |
| M4 | `feat/frontend-s3` | `frontend/src/app/'(events)'/explore-events frontend/src/app/'(events)'/guest-list frontend/src/app/'(events)'/scan frontend/src/app/'(events)'/event-team frontend/src/app/'(events)'/network frontend/src/app/'(overview)' frontend/src/app/_components frontend/src/app/about-us frontend/src/app/contact-us frontend/src/app/'(legal)'` |
| M2 | `feat/qa-s3` | `backend/tests/unit/admission.authz.test.js backend/tests/unit/capacity.test.js backend/tests/unit/guest.parse.test.js backend/tests/unit/nlQuery.test.js backend/tests/unit/networking.authz.test.js backend/tests/unit/networkingOtp.test.js backend/tests/unit/guestList.visibility.test.js backend/tests/fixtures/nlQueryEvalSet.js backend/tests/fixtures/chatbotEvalSet.js` |

#### Exact commands, Sprint 3

**M3, backend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/backend-s3

git checkout origin/import/full-tree -- backend/src/models/guestModel.js backend/src/models/auditLogModel.js backend/src/models/messageModel.js backend/src/repositories/guestRepository.js backend/src/repositories/auditLogRepository.js backend/src/repositories/messageRepository.js
git commit -m "feat(data): guest, audit log and message models

- Guest email is unique per event, so re-importing the same file is
  idempotent rather than duplicating invites
- Audit rows record outcome, reason, device and whether entry was manual
- Manual rows are flagged, because they carry no device fingerprint and
  must be excluded from anomaly detection"

git checkout origin/import/full-tree -- backend/src/services/guestService.js backend/src/services/retentionService.js backend/src/presentation/controllers/guestController.js
git commit -m "feat(guests): guest list import, invites and GDPR erasure

- Each guest is persisted before the invite email is attempted, so a mail
  outage cannot lose the list
- Invalid rows are reported as skipped with a reason, rather than failing
  the whole import
- Guest-list management is refused for public events. hasGuestList is
  defined once on the model and read by both the service and the UI
  lookup, so the browser and the API cannot disagree
- Erasure anonymises name and email but keeps VIP status, plus-ones and
  arrival record, so attendance statistics stay usable"

git checkout origin/import/full-tree -- backend/src/services/admissionService.js backend/src/services/usherService.js backend/src/presentation/controllers/admissionController.js backend/src/presentation/controllers/usherController.js
git commit -m "feat(admission): atomic door check-in with audit trail

- Admission is a conditional update inside a transaction: the status
  guard and the audit row commit together
- Two simultaneous scans of one ticket admit exactly once, and both
  attempts are recorded
- Capacity is checked after admissibility, so re-scanning an admitted
  ticket reports already-admitted rather than venue-full
- Scan authorisation is a pure function: owner, admin, or an usher
  assigned to that specific event. Role alone grants nothing"

git checkout origin/import/full-tree -- backend/src/services/networkingService.js backend/src/services/networkingGuestService.js backend/src/services/networkingNotificationService.js backend/src/presentation/controllers/networkingController.js
git commit -m "feat(networking): Meet and Greet with guest access by code

- Eligibility is a valid booking, not a role, so guests who never made an
  account can take part
- The access-code endpoint returns an identical response whether or not
  the address holds a ticket, otherwise it becomes a way to enumerate
  attendees
- Codes are stored hashed, expire in ten minutes and are single-use"

git push -u origin feat/backend-s3
```

**M5, Data and ML**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/dataml-s3

git checkout origin/import/full-tree -- backend/src/services/chatbot backend/src/presentation/controllers/chatController.js backend/src/presentation/routes/chatRoutes.js
git commit -m "feat(concierge): tool-calling chatbot with provider fallback

- The model never answers from memory: it picks a tool, the service runs
  it against the real repositories, and the model only phrases the result
- So it cannot invent an event, a price or a date
- One function-calling round trip, not a multi-hop agent loop, which
  keeps latency and cost bounded
- OpenAI primary, Gemini fallback, plain fetch and no vendor SDK
- With neither key configured it degrades to a canned reply, not an error"

git checkout origin/import/full-tree -- backend/src/services/weatherService.js
git commit -m "feat(concierge): weather, dress-code and attendance advice

- Open-Meteo geocoding and forecast, no API key required
- Folded into the event-details tool, so one question returns venue,
  tickets, forecast and safety notes together
- If no forecast is available the reply says exactly that, rather than
  guessing one
- Safety notes are framed as practical attendance advice, never as a
  crime or neighbourhood rating, because no such data is held"

git checkout origin/import/full-tree -- backend/src/services/nlGuestQueryService.js backend/src/services/nlQuery backend/src/presentation/controllers/nlQueryController.js backend/src/assets
git commit -m "feat(analytics): natural-language guest query

- Answers count and list questions about a guest list in plain English
- Implemented as a regex intent parser, NOT a language model
- Deliberate data-protection decision: guest names and email addresses
  never leave the process
- Worth stating precisely in the report, since the rest of the AI surface
  does call a third party"

git push -u origin feat/dataml-s3
```

**M4, frontend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/frontend-s3

git checkout origin/import/full-tree -- frontend/src/app/'(events)'/explore-events frontend/src/app/'(overview)' frontend/src/app/_components
git commit -m "feat(discovery): explore, filters, sorting and home carousels

- Categories, removable filter tags, sorting, and trending and upcoming
  carousels
- Filters are tinted down rather than up: a translucent white field over
  the banner put placeholder text at 3.45:1, below the 4.5:1 minimum
- Every value was computed against the worst case under the banner glow,
  rather than chosen by eye"

git checkout origin/import/full-tree -- frontend/src/app/'(events)'/guest-list frontend/src/app/'(events)'/event-team
git commit -m "feat(guests): guest manager and door staff UI

- CSV import with a result summary naming skipped rows and why
- Natural-language guest query box and GDPR erasure control
- A public event reached by a hand-typed URL gets an explanation and a
  link to change its access mode, not a failing page"

git checkout origin/import/full-tree -- frontend/src/app/'(events)'/scan
git commit -m "feat(admission): camera scanner with manual fallback

- Uses the device camera where available, with a typed-code fallback for
  when a QR will not scan
- The typed code is accepted in any case and with or without a leading
  hash, because door staff retype under pressure
- An at-capacity result offers an explicit override rather than silently
  admitting or silently refusing"

git checkout origin/import/full-tree -- frontend/src/app/'(events)'/network frontend/src/app/about-us frontend/src/app/contact-us frontend/src/app/'(legal)'
git commit -m "feat(networking): Meet and Greet UI and static pages

- Attendee directory, public event chat and direct messages over
  server-sent events
- Guests without accounts join with an emailed code
- Legal pages carry the refund policy and the data and privacy statement
  the GDPR position depends on"

git push -u origin feat/frontend-s3
```

**M2, QA**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/qa-s3

git checkout origin/import/full-tree -- backend/tests/unit/admission.authz.test.js backend/tests/unit/capacity.test.js
git commit -m "test(admission): authorisation and capacity decisions

- Covers owner, admin and assigned usher, and the case that must fail: an
  usher scanning an event they are not assigned to
- Capacity tests assert the precedence, venue capacity over ticket
  inventory, and that an already admitted ticket is never reported as a
  capacity failure"

git checkout origin/import/full-tree -- backend/tests/unit/guest.parse.test.js backend/tests/unit/nlQuery.test.js backend/tests/fixtures/nlQueryEvalSet.js backend/tests/fixtures/chatbotEvalSet.js
git commit -m "test(guests): CSV parser and natural-language query intents

- Parser tests include a deliberately invalid row, asserting it is
  reported as skipped rather than crashing the import
- Header row optional and column order free, both covered
- Query tests run against a fixed evaluation set, so intent accuracy is
  measured rather than asserted"

git checkout origin/import/full-tree -- backend/tests/unit/networking.authz.test.js backend/tests/unit/networkingOtp.test.js backend/tests/unit/guestList.visibility.test.js
git commit -m "test(networking): guest access and guest-list visibility

- One-time code tests cover expiry, reuse and a wrong code, and assert
  the response is identical when no booking exists
- Guest-list visibility is pinned in both directions, so a public event
  can never offer a guest list the API would refuse"

git push -u origin feat/qa-s3
```

**Sprint 3 review.** M3 is Scrum Master:

```bash
git checkout main && git pull origin main
git merge --no-ff dev -m "Sprint 3: discovery, guest management, door operations and engagement"
git tag -a v0.3.0-sprint3 -m "Sprint 3 increment"
git push origin main --tags
```

---

### Sprint 4, purchase, live operations, revenue and release

Tag: `v1.0.0-final`. **M4 is Scrum Master.**

| Who | Branch | Paths to take |
|---|---|---|
| M3 | `feat/backend-s4` | `backend/src/models/bookingModel.js backend/src/services/bookingService.js backend/src/services/paymentService.js backend/src/services/pricingService.js backend/src/services/payoutService.js backend/src/services/revenueService.js backend/src/services/dashboardService.js backend/src/repositories/bookingRepository.js backend/src/presentation/controllers/bookingController.js backend/src/presentation/controllers/paymentController.js backend/src/presentation/controllers/dashboardController.js backend/src/presentation/routes/bookingRoutes.js` |
| M5 | `feat/dataml-s4` | `backend/src/services/anomalyService.js backend/src/services/anomalyReportService.js backend/src/services/noShowService.js backend/ml` |
| M4 | `feat/frontend-s4` | `frontend/src/app/checkout frontend/src/app/'(events)'/dashboard frontend/src/app/'(events)'/admin frontend/src/app/my-profile frontend/src/app/api` |
| M2 | `feat/qa-s4` | `backend/tests/ frontend/src/components/ui/digital-ticket.test.tsx frontend/src/components/ui/earnings-trend.test.tsx frontend/src/components/chatbot/formatted-reply.test.tsx frontend/src/utils/event-tabs.test.ts frontend/src/app/'(events)'/scan/'[eventId]'/_component/scanner.test.tsx frontend/e2e` |
| M1 | `feat/devops-s4` | `docs/push-plan.md docs/push-runbook.md docs/azure-devops-setup.sh` |

#### Exact commands, Sprint 4

**M3, backend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/backend-s4

git checkout origin/import/full-tree -- backend/src/models/bookingModel.js backend/src/repositories/bookingRepository.js backend/src/services/bookingService.js
git commit -m "feat(checkout): reservation holds and booking lifecycle

- Inventory is held before the buyer reaches the payment provider, so a
  charge can never exist without a booking behind it
- A hold that is never paid is released and the seats go back on sale, so
  an abandoned checkout costs nothing
- Booking status is a six-state machine, not a boolean. isCheckedIn is
  derived, so there is one source of truth"

git checkout origin/import/full-tree -- backend/src/services/pricingService.js backend/src/services/paymentService.js backend/src/presentation/controllers/paymentController.js
git commit -m "feat(checkout): server-authoritative pricing and confirmation

- The amount is computed on the server from the event own tiers
- It was previously taken from the client, so a buyer could pay any
  figure they liked for any ticket
- The webhook signature is verified against the raw request body, not the
  parsed JSON, because re-serialising changes the bytes
- Confirmation is idempotent and guarded on the pending state, so a
  webhook retry racing the browser callback issues one ticket, not two"

git checkout origin/import/full-tree -- backend/src/services/payoutService.js backend/src/services/revenueService.js
git commit -m "feat(revenue): platform fee, payouts and revenue reporting

- The fee is taken through split settlement, so the organiser is paid
  directly and the fee is deducted at source rather than invoiced
- The subaccount code is select:false and never leaves the server
- Only a masked account name and the last four digits are stored: full
  account numbers would create a liability the system cannot act on
- Admin revenue reports the fee alone, not the gross, which is the number
  the platform actually earns"

git checkout origin/import/full-tree -- backend/src/services/dashboardService.js backend/src/presentation/controllers/dashboardController.js backend/src/presentation/controllers/bookingController.js backend/src/presentation/routes/bookingRoutes.js
git commit -m "feat(dashboard): live arrivals snapshot and stream

- A point-in-time snapshot on connect, then server-sent events, so the
  dashboard is populated before the next scan rather than empty
- The bookings endpoint enforces the same ownership rule as the
  dashboard. It previously checked authentication but not authorisation,
  so any account could read any event attendee list and revenue"

git push -u origin feat/backend-s4
```

**M5, Data and ML**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/dataml-s4

git checkout origin/import/full-tree -- backend/src/services/anomalyService.js backend/src/services/anomalyReportService.js
git commit -m "feat(analytics): scan anomaly detection

- Rules flag repeated rejects, scans from multiple devices, and scans too
  close together to be genuine
- Manual check-ins are excluded: they carry no device fingerprint or scan
  timing, so feeding them to the detector would only manufacture flags
- Runs locally on the audit log. No scan data leaves the process"

git checkout origin/import/full-tree -- backend/src/services/noShowService.js backend/ml
git commit -m "feat(analytics): no-show prediction from portable weights

- Weights are trained offline and shipped as a file, so nothing trains at
  request time and the prediction path stays fast and deterministic
- Both ticket buyers and invited guests are scored, asserted by test.
  Scoring one source would quietly understate the expected gap
- An invited guest VIP status and plus-ones reach the model, because they
  change the likelihood materially"

git push -u origin feat/dataml-s4
```

**M4, frontend**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/frontend-s4

git checkout origin/import/full-tree -- frontend/src/app/checkout frontend/src/app/api
git commit -m "feat(checkout): order summary and payment flow

- Summary lists only the tiers actually chosen, and states the total in
  the event currency with no booking fee added
- The total is the plain sum of tier prices. It previously showed a
  marked-up figure that nobody was ever charged"

git checkout origin/import/full-tree -- frontend/src/app/'(events)'/dashboard
git commit -m "feat(dashboard): live arrivals over server-sent events

- Capacity, sold and admitted counts update as scans arrive, no refresh
- Flagged tickets and expected no-shows surface beside the counts, so the
  organiser sees the warning before the queue forms"

git checkout origin/import/full-tree -- frontend/src/app/my-profile frontend/src/app/'(events)'/admin
git commit -m "feat(profile): tickets, payouts, revenue and admin views

- Payout onboarding with bank selection and account resolution
- Revenue with My events and Platform tabs for admins, where the platform
  figure is the fee alone rather than the gross
- The daily earnings chart is columns, not a line: each value is a total
  accumulated within a day, and a line would assert a figure at an hour
  the data cannot answer for"

git push -u origin feat/frontend-s4
```

**M2, QA**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/qa-s4

git checkout origin/import/full-tree -- backend/tests/
git commit -m "test: integration suite against a real replica set

- Concurrency tests prove the two properties the system depends on: one
  ticket admits exactly once, and the last seat cannot be sold twice
- Run against a real replica set rather than a mock, because both
  guarantees come from the transaction rather than the application code
- Covers checkout splits, payout onboarding, revenue scope, and the Meet
  and Greet notification reaching invited guests and ticket buyers alike"

git checkout origin/import/full-tree -- frontend/src/components/ui/digital-ticket.test.tsx frontend/src/components/ui/earnings-trend.test.tsx frontend/src/components/chatbot/formatted-reply.test.tsx frontend/src/utils/event-tabs.test.ts frontend/src/app/'(events)'/scan/'[eventId]'/_component/scanner.test.tsx frontend/e2e
git commit -m "test(frontend): component and end-to-end coverage

- Pins the parts that regressed before: the QR encoding the scannable
  ticket id, the chart zero baseline and scale choice, and the guest-list
  tab appearing only where a guest list exists
- Chat rendering is asserted to build from React elements, never raw
  HTML, so a model echoing user input cannot inject markup"

git push -u origin feat/qa-s4
```

**M1, DevOps**

```bash
git checkout dev && git pull origin dev
git checkout -b feat/devops-s4

git checkout origin/import/full-tree -- docs/push-plan.md docs/push-runbook.md docs/azure-devops-setup.sh
git commit -m "docs(process): push plan, runbook and board setup

- Records how the repository and the board were configured
- Names the three traps that made a correctly imported board look empty:
  unsubscribed team areas, disabled backlog levels, and an ampersand in
  an area path, which Azure rejects outright"

git push -u origin feat/devops-s4
```

#### Documentation branches

Do these after the four feature branches are merged, so the docs describe a `dev` that
already holds the code. `docs/artefact` is the captured evidence: 42 app-output screenshots,
11 Azure Boards captures and 2 standups, about 12 MB in total.

| Who | Branch | Paths to take |
|---|---|---|
| M2 | `docs/quality` | `docs/usability-test-plan.md docs/accessibility.md docs/quality-model-iso25010.md docs/feature-testing-guide.md docs/market-analysis.md docs/figure-index.md` |
| M2 | `docs/evidence` | `docs/artefact` |
| M1 | `docs/agile` | `docs/agile-sprint-plan.md docs/agile-backlog-import.csv docs/azure-devops-backlog.csv docs/azure-devops-backlog-missing.csv` |
| M3 | `docs/technical` | `docs/technical-documentation.md README.md` |
| M4 | `docs/diagrams` | `docs/architecture-diagram.md docs/use-case-diagram.md docs/data-flow-diagram.md docs/design-models.md docs/diagrams` |

**M2, quality and evidence**

```bash
git checkout dev && git pull origin dev
git checkout -b docs/quality

git checkout origin/import/full-tree -- docs/usability-test-plan.md docs/accessibility.md docs/quality-model-iso25010.md docs/feature-testing-guide.md docs/market-analysis.md docs/figure-index.md
git commit -m "docs(quality): usability, accessibility and ISO 25010 evidence

- Usability protocol and results against ISO 9241-11, with SUS scoring
- WCAG 2.2 AA audit with findings and remediation
- ISO/IEC 25010 quality model mapped to the features that evidence it
- These three answer the brief international quality standards clause,
  which unit tests alone do not"

git push -u origin docs/quality
```

```bash
git checkout dev && git pull origin dev
git checkout -b docs/evidence

git checkout origin/import/full-tree -- docs/artefact
git commit -m "docs(evidence): captured screenshots of board, ceremonies and app

- 42 app-output captures with live data, including the rejected re-scan,
  which demonstrates a correctness property rather than a feature
- 11 Azure Boards captures covering backlog hierarchy, epics, sprint
  boards and work items by assignee
- 2 standup captures, evidencing ceremonies held rather than scheduled"

git push -u origin docs/evidence
```

**M1, agile artefacts**

```bash
git checkout dev && git pull origin dev
git checkout -b docs/agile

git checkout origin/import/full-tree -- docs/agile-sprint-plan.md docs/agile-backlog-import.csv docs/azure-devops-backlog.csv docs/azure-devops-backlog-missing.csv
git commit -m "docs(agile): sprint plan, backlog export and contribution split

- Four sprints, ceremony schedule and the rotating Scrum Master
- Backlog export matching the board: 13 epics, 33 features, 73 items
- Contribution table reported two ways, by effort and by involvement,
  because the two tell different and equally true stories"

git push -u origin docs/agile
```

**M3, technical documentation**

```bash
git checkout dev && git pull origin dev
git checkout -b docs/technical

git checkout origin/import/full-tree -- docs/technical-documentation.md README.md
git commit -m "docs(technical): architecture, data model and implementation map

- Every claim cites the file it is traceable to, so the document can be
  checked against the source rather than taken on trust
- Records the defects found and closed, including the two access-control
  failures, because a found-and-fixed vulnerability is stronger evidence
  than a clean report"

git push -u origin docs/technical
```

**M4, diagrams**

```bash
git checkout dev && git pull origin dev
git checkout -b docs/diagrams

git checkout origin/import/full-tree -- docs/architecture-diagram.md docs/use-case-diagram.md docs/data-flow-diagram.md docs/design-models.md docs/diagrams
git commit -m "docs(diagrams): rendered diagram set with editable sources

- Use case, architecture, data flow, class, package, state and sequence
  diagrams
- Every diagram exists as an image as well as source, because a fenced
  mermaid block renders as raw text in a PDF or Word export, which is how
  the work is submitted
- Graphviz sources for the two hand-laid diagrams, draw.io for the rest"

git push -u origin docs/diagrams
```

> **`docs/diagrams/node_modules` is git-ignored**, so the 425 MB diagram toolchain does not
> travel. Check `git status --short docs/diagrams | head` before committing: hundreds of files
> means the ignore rule did not travel, and you must stop.

**Two files deliberately unassigned.** `backend/notes` and `backend/users.csv` are scratch
files with no purpose in the submission. Delete rather than commit them:

```bash
rm -f backend/notes backend/users.csv
```

**Sprint 4 review.** M4 is Scrum Master:

```bash
git checkout main && git pull origin main
git merge --no-ff dev -m "Sprint 4: purchase, live operations, revenue and release"
git tag -a v1.0.0-final -m "Final increment"
git push origin main --tags
```

---

## Phase E. Close out

**E1.** After the Sprint 4 merge and tag, delete the staging branch so it is never a route
into `main`:

```bash
git push origin --delete import/full-tree
```

**E2.** Confirm nothing was missed. On any laptop:

```bash
git checkout main && git pull origin main
git diff --stat origin/import/full-tree
```

**Before deleting the staging branch**, run that diff. Empty output means `main` holds
everything. Any file listed was never taken by anyone, so assign it and commit it before E1.

**E3.** Confirm the sprint structure:

```bash
git log --oneline --graph --first-parent main
```

Four merge commits, four tags.

**E4.** Confirm the contribution record:

```bash
git shortlog -sne --no-merges
```

This must agree with the table in `agile-sprint-plan.md` §8. If it does not, change the table.

---

## If something goes wrong

| Symptom | Fix |
|---|---|
| `git push` rejected, "fetch first" | `git pull --rebase origin <branch>` then push again |
| Committed with the wrong email, not yet pushed | `git commit --amend --reset-author` after fixing `git config user.email` |
| Committed with the wrong email, already pushed | Leave it. Rewriting shared history breaks everyone else's clone. Note it in the report. |
| Took the wrong paths, not yet committed | `git restore --staged . && git checkout -- .` |
| Merge conflict on `dev` | `git pull origin dev`, resolve, `git add`, `git commit` |
| A path is missing from the tables | `git checkout origin/import/full-tree -- <path>` on the closest owner's branch |

**One thing not to do.** Do not `git add -A` on your branch. It stages the whole tree,
including other people's files, and produces the ninety-file commit this runbook exists to
avoid. Always name your paths explicitly.
