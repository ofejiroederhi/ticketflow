#!/usr/bin/env python3
"""
Rebuilds the Azure Boards backlog from azure-devops-backlog.csv.

Exists because the board was destroyed on 12 August 2026 and had to be recreated. The CSV is
the source of truth for the 73 backlog items and 198 tasks; the epics, features and the parent
links between the levels are defined here, because CSV import cannot express a hierarchy above
backlog-item level.

Creates, in order:
  1. 13 Epics
  2. 33 Features, each parented to its Epic
  3. 73 Product Backlog Items from the CSV, each parented to its Feature
  4. 198 Tasks from the CSV, each parented to its backlog item

Every item carries its area path, iteration path, assignee, tags and effort or activity from
the CSV, so the rebuilt board is identical to the original apart from the work item IDs, which
Azure allocates from an organisation-wide sequence and cannot be chosen.

    python3 docs/rebuild-board.py            # rebuild
    python3 docs/rebuild-board.py --verify   # count only, changes nothing
"""

import csv
import json
import pathlib
import subprocess
import sys

ORG = "https://dev.azure.com/ijeomac"
PROJECT = "7003SCN Advanced Software Developmet Group 2"
CSV = pathlib.Path(__file__).parent / "azure-devops-backlog.csv"

EPICS = [
    ("E1-Accounts", "E1 Accounts and access"),
    ("E2-Events", "E2 Event management"),
    ("E3-Sales", "E3 Ticket sales"),
    ("E4-Admission", "E4 Admission"),
    ("E5-Guests", "E5 Guest management"),
    ("E6-LiveOps", "E6 Live operations"),
    ("E7-Intelligence", "E7 Intelligence"),
    ("E8-Quality", "E8 Quality and compliance"),
    ("E9-Networking", "E9 Attendee networking"),
    ("E10-Concierge", "E10 AI concierge"),
    ("E11-Discovery", "E11 Discovery"),
    ("E12-Revenue", "E12 Revenue"),
    ("E13-Process", "E13 Process and facilitation"),
]

# (epic tag, feature name, [backlog item titles it owns, matched on the CSV Title 1 column])
# Matching is on a distinctive prefix rather than the whole title, so a wording tweak in the
# CSV does not silently orphan a feature.
FEATURES = [
    ("E1-Accounts", "Registration and authentication", ["As a visitor I can register", "As a registered user I can log in", "As a user I can reset a forgotten"]),
    ("E1-Accounts", "Role-based access control", ["As an administrator I can assign roles", "As an administrator I can list and deactivate", "As the team we seed the first"]),
    ("E1-Accounts", "Profile management", ["As a user I can update my profile", "As a user I can delete my own"]),
    ("E2-Events", "Event creation and authoring", ["As an organiser I can access a dedicated", "As an organiser I can create a new", "As an organiser I can enter a title", "As an organiser I can set the start date", "As an organiser I can upload a primary", "As an organiser I can attach social", "As an organiser I can post the event"]),
    ("E2-Events", "Event configuration and access modes", ["As an organiser I can set the event access", "As an organiser I can record venue", "As an organiser I can set venue capacity", "As an organiser I can enter the event location"]),
    ("E2-Events", "Event lifecycle management", ["As an organiser I can edit an event", "As an organiser I can see my own events", "As an administrator I can archive"]),
    ("E3-Sales", "Ticket configuration", ["As an organiser I can set opening and closing", "As an organiser I can define ticket tiers", "As an organiser I can choose the ticket currency"]),
    ("E3-Sales", "Checkout and payment", ["As an attendee I can review my order", "As an attendee I can choose a payment", "As an attendee I receive a receipt", "As a visitor I can buy a ticket without"]),
    ("E3-Sales", "Ticket issuance and inventory integrity", ["As an attendee I can open my ticket", "As an organiser inventory is held", "As the platform every order is priced"]),
    ("E4-Admission", "QR scanning and atomic check-in", ["As door staff I can scan a ticket", "As an organiser the door refuses", "As door staff I can admit manually"]),
    ("E4-Admission", "Capacity safety and door staff", ["As an organiser the door stops admitting", "As an organiser I can assign door staff"]),
    ("E5-Guests", "Guest list import", ["As an organiser I can import a guest list", "As an organiser I can add a single guest", "As an organiser I only see the guest list"]),
    ("E5-Guests", "Invite issuance", ["As a guest I receive a single-use"]),
    ("E5-Guests", "GDPR erasure", ["As an organiser I can erase a guest"]),
    ("E6-LiveOps", "Arrivals dashboard and real-time streaming", ["As an organiser I can watch arrivals"]),
    ("E7-Intelligence", "Natural-language guest queries", ["As an organiser I can ask questions about my guest"]),
    ("E7-Intelligence", "Anomaly detection", ["As an organiser I can review scan anomalies"]),
    ("E7-Intelligence", "No-show prediction", ["As an organiser I see expected no-shows"]),
    ("E8-Quality", "CI/CD and containerisation", ["As the team every push is verified", "As the team we can run the whole stack", "As the team the stack can be deployed"]),
    ("E8-Quality", "Security and access-control assurance", ["As an organiser only I or an admin"]),
    ("E8-Quality", "Documentation, coverage and demonstration", ["As the team the product is documented", "As the team coverage is measured"]),
    ("E9-Networking", "Meet and Greet directory and chat", ["As an attendee I can join Meet and Greet", "As an attendee I can opt in to the directory"]),
    ("E9-Networking", "Guest access by one-time code", ["As a guest without an account"]),
    ("E9-Networking", "Networking notifications", ["As an organiser I am notified when Meet"]),
    ("E10-Concierge", "Chatbot with tool calling", ["As a visitor I can ask a concierge"]),
    ("E10-Concierge", "Weather and dress-code advice", ["As an attendee I can ask what to wear"]),
    ("E11-Discovery", "Categories, filters and sorting", ["As a visitor I can open a panel", "As a visitor I can see the active filter", "As a visitor I can sort search results"]),
    ("E11-Discovery", "Search, trending and upcoming", ["As a visitor I can browse trending", "As a visitor I can search events by name"]),
    ("E11-Discovery", "Event detail page", ["As a visitor I can click an event"]),
    ("E12-Revenue", "Platform fee and payouts", ["As the platform we take a percentage", "As an organiser I can connect a payout"]),
    ("E12-Revenue", "Revenue reporting", ["As an organiser I can see my revenue", "As an administrator I can see platform fee"]),
    ("E13-Process", "Sprint facilitation", ["Chair Sprint"]),
    ("E13-Process", "Retrospectives and Definition of Done", ["Facilitate the retrospectives"]),
]


def az(args, capture=True):
    """Run an az command, returning parsed JSON or None."""
    cmd = ["az"] + args + ["--organization", ORG, "--project", PROJECT]
    if capture:
        cmd += ["-o", "json"]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout) if capture and r.stdout.strip() else True
    except json.JSONDecodeError:
        return True


def create(wtype, title, fields=None):
    args = ["boards", "work-item", "create", "--type", wtype, "--title", title[:255]]
    if fields:
        args += ["--fields"] + [f"{k}={v}" for k, v in fields.items() if v not in (None, "")]
    out = az(args)
    return out.get("id") if isinstance(out, dict) else None


def link(child, parent):
    return az(["boards", "work-item", "relation", "add", "--id", str(child),
               "--relation-type", "parent", "--target-id", str(parent)]) is not None


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    pbis = [r for r in rows if r["Work Item Type"] == "Product Backlog Item"]
    print(f"Source: {len(pbis)} backlog items, {len(rows) - len(pbis)} tasks\n")

    if "--verify" in sys.argv:
        return

    # 1. Epics
    epic_id = {}
    print("Epics")
    for tag, name in EPICS:
        i = create("Epic", name, {"System.AreaPath": PROJECT})
        epic_id[tag] = i
        print(f"  #{i}  {name}")

    # 2. Features, parented to their epic
    print("\nFeatures")
    feat_id = {}
    for tag, name, _ in FEATURES:
        i = create("Feature", name, {"System.AreaPath": PROJECT})
        feat_id[name] = i
        link(i, epic_id[tag])
        print(f"  #{i}  {name}")

    # Which feature owns a given backlog item title.
    def feature_for(title):
        for _, name, prefixes in FEATURES:
            if any(title.startswith(p) for p in prefixes):
                return feat_id[name]
        return None

    # 3. Backlog items, then 4. their tasks. Walked in file order so each task attaches to the
    # backlog item above it, which is how the CSV encodes the hierarchy.
    print("\nBacklog items and tasks")
    current, made_p, made_t, orphan = None, 0, 0, []
    for r in rows:
        common = {
            "System.AreaPath": r["Area Path"],
            "System.IterationPath": r["Iteration Path"],
            "System.AssignedTo": r["Assigned To"],
            "System.Tags": r["Tags"].replace(";", "; "),
            "System.Description": r["Description"],
        }
        if r["Work Item Type"] == "Product Backlog Item":
            f = {**common, "Microsoft.VSTS.Common.AcceptanceCriteria": r["Acceptance Criteria"],
                 "Microsoft.VSTS.Scheduling.Effort": r["Effort"],
                 "Microsoft.VSTS.Common.Priority": r["Priority"]}
            current = create("Product Backlog Item", r["Title 1"], f)
            made_p += 1
            parent = feature_for(r["Title 1"])
            if parent:
                link(current, parent)
            else:
                orphan.append(r["Title 1"][:60])
            if made_p % 10 == 0:
                print(f"  {made_p} backlog items, {made_t} tasks")
        else:
            f = {**common, "Microsoft.VSTS.Common.Activity": r["Activity"]}
            t = create("Task", r["Title 2"], f)
            if t and current:
                link(t, current)
            made_t += 1

    print(f"\nCreated: {len(epic_id)} epics, {len(feat_id)} features, "
          f"{made_p} backlog items, {made_t} tasks")
    if orphan:
        print("Backlog items with no matching feature:")
        for o in orphan:
            print("  ", o)


if __name__ == "__main__":
    main()
