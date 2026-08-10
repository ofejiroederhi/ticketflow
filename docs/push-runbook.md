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
git checkout -b develop && git push -u origin develop
```

**A7.** On GitHub: **Settings, Collaborators**, add the other four with **Write** access.

**A8.** On GitHub: **Settings, Branches, Add branch protection rule** for `main`. Tick
*Require a pull request before merging* and set *Required approvals* to **1**.

> Do **not** protect `develop`. Protecting both means every commit needs someone else awake,
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

The loop is identical every sprint. Only the paths change.

### The loop, in general

Every member, every sprint:

```bash
# 1. Start from the latest develop
git checkout develop && git pull origin develop

# 2. Branch for this sprint's work
git checkout -b feat/<area>-s<N>

# 3. Take your paths out of the staging branch
git checkout origin/import/full-tree -- <your paths for this sprint>

# 4. Commit, in two or three steps rather than one
git commit -m "feat(<area>): <what it does>

AB#<id> AB#<id>"

# 5. Push
git push -u origin feat/<area>-s<N>
```

Then open a pull request into `develop` on GitHub, ask the member named in the `Pair-` tag to
approve it, merge, and delete the branch.

> **Commit in two or three steps, not one.** After step 3 the files are staged. Commit a
> coherent slice, then `git add` the next slice and commit again. A member with fifteen
> commits across four sprints reads as work. One commit of ninety files does not.

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

M3's exact commands, as a worked example:

```bash
git checkout develop && git pull origin develop
git checkout -b feat/backend-s1
git checkout origin/import/full-tree -- backend/package.json backend/package-lock.json backend/src/shared backend/src/models/userModel.js
git commit -m "feat(backend): project skeleton, shared utilities and user model

AB#602"
git checkout origin/import/full-tree -- backend/src/services/authService.js backend/src/services/userService.js backend/src/repositories/userRepository.js
git commit -m "feat(auth): registration, login, password reset and role whitelist

AB#602 AB#607 AB#611 AB#615"
git checkout origin/import/full-tree -- backend/src/presentation backend/server.js backend/app.js
git commit -m "feat(api): routes, controllers and security middleware

AB#627 AB#631"
git push -u origin feat/backend-s1
```

**Sprint 1 review.** M1 is Scrum Master. Once all four PRs are merged into `develop`:

```bash
git checkout main && git pull origin main
git merge --no-ff develop -m "Sprint 1: accounts, roles, profiles, CI and containers"
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

---

### Sprint 3, discovery, guests, door operations and engagement

Tag: `v0.3.0-sprint3`. **M3 is Scrum Master.** The largest sprint, 132 points.

| Who | Branch | Paths to take |
|---|---|---|
| M3 | `feat/backend-s3` | `backend/src/models/guestModel.js backend/src/models/auditLogModel.js backend/src/models/messageModel.js backend/src/services/guestService.js backend/src/services/admissionService.js backend/src/services/usherService.js backend/src/services/networkingService.js backend/src/services/networkingGuestService.js backend/src/services/networkingNotificationService.js backend/src/services/retentionService.js backend/src/repositories/guestRepository.js backend/src/repositories/auditLogRepository.js backend/src/repositories/messageRepository.js backend/src/presentation/controllers/admissionController.js backend/src/presentation/controllers/guestController.js backend/src/presentation/controllers/usherController.js backend/src/presentation/controllers/networkingController.js` |
| M5 | `feat/dataml-s3` | `backend/src/services/chatbot backend/src/services/nlQuery backend/src/services/nlGuestQueryService.js backend/src/services/weatherService.js backend/src/presentation/controllers/chatController.js backend/src/presentation/controllers/nlQueryController.js backend/src/presentation/routes/chatRoutes.js backend/src/assets` |
| M4 | `feat/frontend-s3` | `frontend/src/app/'(events)'/explore-events frontend/src/app/'(events)'/guest-list frontend/src/app/'(events)'/scan frontend/src/app/'(events)'/event-team frontend/src/app/'(events)'/network frontend/src/app/'(overview)' frontend/src/app/_components frontend/src/app/about-us frontend/src/app/contact-us frontend/src/app/'(legal)'` |
| M2 | `feat/qa-s3` | `backend/tests/unit/admission.authz.test.js backend/tests/unit/capacity.test.js backend/tests/unit/guest.parse.test.js backend/tests/unit/nlQuery.test.js backend/tests/unit/networking.authz.test.js backend/tests/unit/networkingOtp.test.js backend/tests/unit/guestList.visibility.test.js backend/tests/fixtures/nlQueryEvalSet.js backend/tests/fixtures/chatbotEvalSet.js` |

**M5's first sprint with code.** Worked example:

```bash
git checkout develop && git pull origin develop
git checkout -b feat/dataml-s3
git checkout origin/import/full-tree -- backend/src/services/chatbot backend/src/presentation/controllers/chatController.js backend/src/presentation/routes/chatRoutes.js
git commit -m "feat(concierge): tool-calling chatbot with provider fallback

AB#729"
git checkout origin/import/full-tree -- backend/src/services/weatherService.js
git commit -m "feat(concierge): weather, dress-code and attendance advice

AB#734"
git checkout origin/import/full-tree -- backend/src/services/nlGuestQueryService.js backend/src/services/nlQuery backend/src/presentation/controllers/nlQueryController.js
git commit -m "feat(analytics): natural-language guest query, regex intent parser

AB#754"
git push -u origin feat/dataml-s3
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

**Documentation, split by who owns the subject.** Do this after the four feature branches
are merged, so the docs describe a `develop` that already holds the code.

| Who | Branch | Paths to take |
|---|---|---|
| M2 | `docs/quality` | `docs/usability-test-plan.md docs/accessibility.md docs/quality-model-iso25010.md docs/feature-testing-guide.md docs/market-analysis.md docs/report/figure-index.md` |
| M2 | `docs/evidence` | `docs/artefact` (55 screenshots: 42 app output, 11 Azure Boards, 2 standups) |
| M1 | `docs/agile` | `docs/agile-sprint-plan.md docs/agile-backlog-import.csv docs/azure-devops-backlog.csv docs/azure-devops-backlog-missing.csv` |
| M3 | `docs/technical` | `docs/technical-documentation.md README.md` |
| M4 | `docs/diagrams` | `docs/architecture-diagram.md docs/use-case-diagram.md docs/data-flow-diagram.md docs/design-models.md docs/diagrams` |

Each opens a PR into `develop` as usual. M4's is the largest because `docs/diagrams` carries
every rendered PNG and SVG plus the Graphviz and draw.io sources.

`docs/artefact` is the captured evidence the report is built from, so it belongs with QA. It is
about 12 MB of PNGs; commit it in one go and check the pack size afterwards.

> **`docs/diagrams/node_modules` is git-ignored**, so the diagram toolchain (about 425 MB of
> Chromium and WebAssembly) does not travel. Only the rendered images and their sources do.
> Confirm with `git status --short docs/diagrams | head` before committing: if you see
> hundreds of files, the ignore rule did not travel and you must stop.

**Two files that are deliberately unassigned.** `backend/notes` and `backend/users.csv` are
scratch files with no owner and no purpose in the submission. Delete them rather than commit
them:

```bash
git rm --cached backend/notes backend/users.csv 2>/dev/null; rm -f backend/notes backend/users.csv
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
| Merge conflict on `develop` | `git pull origin develop`, resolve, `git add`, `git commit` |
| A path is missing from the tables | `git checkout origin/import/full-tree -- <path>` on the closest owner's branch |

**One thing not to do.** Do not `git add -A` on your branch. It stages the whole tree,
including other people's files, and produces the ninety-file commit this runbook exists to
avoid. Always name your paths explicitly.
