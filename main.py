import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def fetch_issues():
    response = requests.get(API_URL, headers=HEADERS)
    issues = response.json()
    return [i for i in issues if "pull_request" not in i]


# --- CLASSIFICATION ---

def classify_issue_type(title):
    title = title.lower()
    if title.startswith("bug:"):
        return "Bug"
    if title.startswith("feature:"):
        return "Feature"
    return "Other"


# --- HEURISTICS ---

def is_high_priority_bug(issue):
    return (
        classify_issue_type(issue["title"]) == "Bug"
        and "High" in (issue.get("body") or "")
    )


def is_vague_title(title):
    vague_words = ["fix issue", "improve", "update", "thing", "stuff"]
    title_lower = title.lower()
    return any(word in title_lower for word in vague_words)


def is_large_story(body):
    if not body:
        return True
    return body.count("- [ ]") > 5


def has_section(body, section):
    if not body:
        return False
    return f"## {section}".lower() in body.lower()


def calculate_readiness_score(issue):
    body = issue.get("body") or ""

    score = 0

    if has_section(body, "Acceptance Criteria"):
        score += 3
    if has_section(body, "Priority"):
        score += 2
    if has_section(body, "Potential Subtasks"):
        score += 2
    if has_section(body, "User Value"):
        score += 2

    if not is_vague_title(issue["title"]):
        score += 1

    return score


def get_ticket_issues(issue):
    problems = []

    title = issue.get("title", "")
    body = issue.get("body") or ""

    # Missing sections
    if "## Acceptance Criteria".lower() not in body.lower():
        problems.append("Missing Acceptance Criteria")

    if "## Priority".lower() not in body.lower():
        problems.append("Missing Priority")

    if "## Potential Subtasks".lower() not in body.lower():
        problems.append("Missing Potential Subtasks")

    if classify_issue_type(title) == "Feature" and "## User Value".lower() not in body.lower():
        problems.append("Missing User Value")

    # Weak title
    if is_vague_title(title):
        problems.append("Vague Title")

    # Weak summary
    if "## Summary" in body:
        summary_section = body.split("## Summary")[-1][:150]
        if len(summary_section.strip()) < 40:
            problems.append("Weak Summary")

    # Too large
    if is_large_story(body):
        problems.append("Likely Too Large")

    return problems


# --- ANALYSIS ---

def analyze_issues(issues):
    sprint_candidates = []
    high_priority_bugs = []
    diagnostics = []

    for issue in issues:
        title = issue["title"]
        number = issue["number"]

        score = calculate_readiness_score(issue)
        problems = get_ticket_issues(issue)

        if is_high_priority_bug(issue):
            high_priority_bugs.append((number, title))

        if problems:
            diagnostics.append((number, title, problems))

        if score >= 7:
            sprint_candidates.append((number, title, score))

    return {
        "high_priority_bugs": high_priority_bugs,
        "diagnostics": diagnostics,
        "sprint_candidates": sorted(sprint_candidates, key=lambda x: -x[2])[:5],
    }

# --- OUTPUT ---

def print_report(results):
    print("\n=== Agentic Product Ops: v2.1 Diagnostics Report ===\n")

    print("🔥 High Priority Bugs:")
    for i in results["high_priority_bugs"]:
        print(f"  - #{i[0]}: {i[1]}")
    if not results["high_priority_bugs"]:
        print("  - None")

    print("\n⚠️ Ticket Diagnostics:")
    for number, title, problems in results["diagnostics"]:
        print(f"\n  #{number}: {title}")
        for p in problems:
            print(f"    - {p}")
    if not results["diagnostics"]:
        print("  - None")

    print("\n🎯 Suggested Sprint Candidates:")
    for i in results["sprint_candidates"]:
        print(f"  - #{i[0]}: {i[1]} (Score: {i[2]})")
    if not results["sprint_candidates"]:
        print("  - None")

    print("\n=== End Report ===\n")


def main():
    issues = fetch_issues()
    results = analyze_issues(issues)
    print_report(results)


if __name__ == "__main__":
    main()