# Push Plan, Fresh Repository

**Situation.** The repository has been re-initialised: **zero commits, zero tracked files**,
546 files waiting in the working tree. Every commit in the final history will therefore be
created from here, which makes this the one moment where the contribution record can be got
right, and the one moment where it can be got badly wrong.

---

## 0. Three blockers, before anyone pushes anything

### 0.1 Two files must never reach a hosted repository

`docs/report/` currently holds material that would be published the moment the repo goes to
GitHub:

| File | Size | Why it cannot be pushed |
|---|---|---|
| `Assessment Brief.pdf` | 467 KB | Its own first line: *"This document is intended for Coventry University Group students for their own use... **It must not be passed to third parties or posted on any website.**"* Pushing it to GitHub is posting it on a website. |
| `sample report.pdf` | 21 MB | Another team's submitted coursework. Republishing it is a copyright problem and, in an academic-integrity review, a very awkward thing to have in your history. |
| `Report-Group2.docx` | 3.3 MB | Your own draft. Not forbidden, but a binary that changes on every edit and bloats history for no benefit. Keep it in OneDrive or Teams. |

Add before the first commit:

```bash
printf 'docs/report/*.pdf\ndocs/report/*.docx\n' >> .gitignore
```

Git history is permanent in practice. A file removed in a later commit is still in the pack,
still clonable, and still there when a marker or an integrity panel looks. Ignore them now,
not after.

### 0.2 Secrets: already safe, verify anyway

`backend/config.env` and `frontend/.env.local` are **already ignored**, and I confirmed that
with `git check-ignore`. Before the first push, confirm nothing else carries a live key:

```bash
git add -A && git grep -nIE "(sk_live|sk_test|AIza|SG\.|mongodb\+srv://[^ ]*:[^ @]*@)" -- ':!*.md' || echo "clean"
```

If that prints nothing, the staged tree carries no obvious secret. Rotate the Paystack test
key and the Gmail app password anyway if either has ever been pasted into a chat or a doc.

### 0.3 One giant "initial commit" destroys the evidence

546 files in a single commit by a single author produces a history that says one person made
the entire product in one action. That is the opposite of what Task 1.1 is marked on, and it
cannot be fixed later without rewriting history.

---

## 1. The authorship question, stated once

Since no history exists, **every commit will be authored now, by whoever runs the command.**
Two things follow.

**What is legitimate:** each member committing and pushing the work they actually did, and
`Co-authored-by:` trailers where two people genuinely worked on something together.

**What is not:** distributing one person's work across five accounts so the graph looks even.
The repository is assessed evidence. A marker can compare commit content, size and timestamps
against the claimed split, and an even distribution created in one evening from a finished
codebase does not survive that comparison. It also puts the whole group at risk over marks
that an honest account would have earned anyway.

`agile-sprint-plan.md` §8 already makes the honest argument well: the split is uneven, story
points measure facilitation, acceptance criteria and accessibility work badly, and total
involvement is far flatter than effort points suggest. Push the history that matches it.

**If the work genuinely was shared**, the plan below is exactly how to record that. **If it
genuinely was not**, push it as it is, and let §8 carry the explanation.

---

## 2. Ownership map

Straight from the Azure Boards area paths, so the repository and the board tell the same
story. Each member owns the paths for the work items assigned to them.

| Member | Account | Area | Paths they commit |
|---|---|---|---|
| **M1 Ijeoma** | `ijeomac` | DevOps | `.github/workflows/`, `docker-compose.yml`, `*/Dockerfile`, `*/.dockerignore`, `backend/scripts/` |
| **M2 Abiola** | `abiolao5` | QA · PO · UX | `backend/tests/`, `frontend/**/*.test.tsx`, `docs/usability-test-plan.md`, `docs/accessibility.md`, `docs/quality-model-iso25010.md`, `docs/market-analysis.md`, `docs/report/figure-index.md` |
| **M3 Ederhi** | `ederhio` | Backend | `backend/src/` except the Data and ML services below |
| **M4 Adetunji** | `adetunjim` | Frontend | `frontend/src/`, `frontend/public/`, config |
| **M5 Akoki** | `akokic` | Data & ML | `backend/src/services/chatbot/`, `anomalyService.js`, `anomalyReportService.js`, `noShowService.js`, `nlGuestQueryService.js`, `weatherService.js`, `backend/ml/` |

Shared documentation (`README.md`, `technical-documentation.md`, the diagram set) belongs to
whoever wrote it. If that was genuinely collaborative, commit it with `Co-authored-by:`.

---

## 3. Every developer works on their own laptop

Nobody switches user. Each of the five is already themselves on their own machine. The only
thing that has to be right is that **git knows who they are in this repository**, because a
laptop with a stale or personal global config will attribute the commits to the wrong person,
and that is the one thing this whole exercise is trying to get right.

Each member, once, on their own laptop:

```bash
git clone git@github.com:ofejiroederhi/ticketflow.git ticketflow && cd ticketflow
```

Then set the identity **per repository**, not globally, so nothing on their machine
interferes:

```bash
git config user.name "Ada Ijeoma" && git config user.email "ijeomac@uni.coventry.ac.uk"
```

The email must be the one attached to their GitHub account, or GitHub will not link the
commits to their profile and the contributors graph will show a stranger. Verify before the
first real commit:

```bash
git config user.email && git log -1 --format='%an <%ae>' 2>/dev/null
```

**The one asymmetry.** Only M3's laptop currently has the code. The other four clone an empty
repository. Section 5 is how they get their own files without anyone emailing a zip.

---

## 4. Branching model, and where sprints merge

Three levels, which is the least that still evidences four increments.

| Branch | Purpose | Who merges into it |
|---|---|---|
| `main` | Submission-ready. **Receives exactly one merge per sprint, at the sprint review.** Protected. | The sprint's Scrum Master |
| `develop` | Integration. Everything lands here during a sprint. | Any member, via reviewed PR |
| `feat/<area>-<item>` | One work item or a coherent slice of one. Short-lived. | n/a, merged and deleted |

**`main` gets four merges, one per sprint.** That is the point of the model: `git log main`
then reads as four increments matching the sprint calendar, rather than a flat stream. Each
merge is tagged, so the increment has a name a report can cite.

| Sprint | Dates | Merge `develop` into `main` at the review | Tag |
|---|---|---|---|
| 1 | 20 to 26 Jul | Sun 26 Jul | `v0.1.0-sprint1` |
| 2 | 27 Jul to 2 Aug | Sun 02 Aug | `v0.2.0-sprint2` |
| 3 | 3 to 9 Aug | Sun 09 Aug | `v0.3.0-sprint3` |
| 4 | 10 to 15 Aug | Sat 15 Aug | `v1.0.0-final` |

The Scrum Master for that sprint runs the merge, which is another way the rotation in
`agile-sprint-plan.md` §2 shows up as evidence rather than assertion.

**On dates, one thing to be straight about.** The repository is being created now, so commit
timestamps will be the real dates on which the commits are made, not the sprint dates above.
Do not rewrite them. Azure Boards is the primary record of when work happened, which
`agile-sprint-plan.md` already states, and a git history with plausible-looking forged
timestamps is far more damaging under scrutiny than one that is simply late.

---

## 5. Getting each member's code onto their own laptop

The problem: four laptops have nothing. The wrong fix is emailing a zip and having each person
`git add -A`, which produces four commits that each touch all 544 files.

**M3 pushes the full tree once, to a staging branch nobody ever merges:**

```bash
git checkout -b import/full-tree
git add -A && git commit -m "chore: import working tree (staging only, never merged)"
git push -u origin import/full-tree
```

**Every other member then takes only their own paths.** On their own laptop, on their own
branch:

```bash
git fetch origin
git checkout -b feat/frontend-app-router origin/develop
git checkout origin/import/full-tree -- frontend/src frontend/public
git commit -m "feat(frontend): app router structure, checkout and scanner

AB#798 AB#802 AB#806"
git push -u origin feat/frontend-app-router
```

`git checkout <ref> -- <paths>` copies exactly those paths out of the staging branch and
stages them. The commit therefore contains only that member's files, authored by them, on
their machine. Nobody switches identity and nobody sends a zip.

Delete the staging branch once all five have taken their slice, so it never appears as a
route into `main`:

```bash
git push origin --delete import/full-tree
```

---

## 6. The sprint cycle, repeated four times

Same loop each sprint. Everything below happens on each member's own laptop.

**During the sprint**, per work item:

```bash
git checkout develop && git pull
git checkout -b feat/backend-atomic-admission
# work, then:
git commit -m "feat(admission): atomic single-use claim inside a transaction

AB#762 AB#767"
git push -u origin feat/backend-atomic-admission
```

Open a PR into `develop`. **The reviewer is the member named in the `Pair-` tag** on that work
item, so the review record matches the board instead of contradicting it. Squash or merge,
then delete the branch.

**At the sprint review**, the sprint's Scrum Master:

```bash
git checkout main && git pull
git merge --no-ff develop -m "Sprint 1: accounts, roles, profiles, CI and containers"
git tag -a v0.1.0-sprint1 -m "Sprint 1 increment"
git push origin main --tags
```

`--no-ff` is deliberate. A fast-forward merge leaves no merge commit, and the sprint boundary
disappears from the graph, which is the one thing this model exists to show.

**Commit granularity matters more than people expect.** Five or six commits per member per
sprint reads as work. One commit of ninety files does not, whoever authored it.

---

## 7. Verification, before you call it done

```bash
git log --oneline --graph --first-parent main
```

Should show four merge commits, one per sprint, each tagged.

```bash
git shortlog -sne --no-merges
```

Commits per author. **This must match the contribution table in `agile-sprint-plan.md` §8. If
it does not, change the table, not the history.** The table is a claim; the history is
evidence.

```bash
git count-objects -vH | grep size-pack
```

Expect well under 50 MB. Larger means a binary slipped in, most likely one of the PDFs from
§0.1.

---

## 8. Checklist

**Before the first push**

- [ ] `docs/report/*.pdf` and `*.docx` in `.gitignore` (done)
- [ ] Secret scan clean; keys rotated if ever shared
- [ ] `main` and `develop` created; `main` protected, PR review required

**Each member, once, on their own laptop**

- [ ] Cloned the repo
- [ ] `git config user.name` and `user.email` set **per repository**, email matching GitHub
- [ ] Verified attribution on their first commit

**Getting the code out**

- [ ] M3 pushed `import/full-tree`
- [ ] Each member took only their own paths onto their own branch
- [ ] Staging branch deleted

**Every sprint, four times**

- [ ] Feature branches off `develop`, PR reviewed by the paired member
- [ ] Several commits per member, not one
- [ ] `AB#<id>` work item links in commit messages
- [ ] Scrum Master merged `develop` into `main` with `--no-ff` and tagged it

**Finally**

- [ ] `git log --first-parent main` shows four tagged sprint merges
- [ ] `git shortlog -sne` agrees with the contribution table
- [ ] Pack size under 50 MB
