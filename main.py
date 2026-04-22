import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

if not GITHUB_TOKEN or not GITHUB_OWNER or not GITHUB_REPO:
    raise ValueError("Missing GITHUB_TOKEN, GITHUB_OWNER, or GITHUB_REPO in .env")

API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def fetch_issues():
    response = requests.get(API_URL, headers=HEADERS, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch issues. Status: {response.status_code}\n{response.text}"
        )

    issues = response.json()

    # Filter out pull requests just in case
    issues = [issue for issue in issues if "pull_request" not in issue]

    return issues


def classify_issue_type(title: str) -> str:
    title_lower = title.lower()

    if title_lower.startswith("bug:"):
        return "Bug"
    if title_lower.startswith("feature:"):
        return "Feature"
    if title_lower.startswith("task:"):
        return "Task"
    if title_lower.startswith("spike:"):
        return "Spike"

    return "Unknown"


def has_section(body: str, section_name: str) -> bool:
    if not body:
        return False
    return f"## {section_name}".lower() in body.lower()


def missing_acceptance_criteria(body: str) -> bool:
    if not body:
        return True

    if "## Acceptance Criteria".lower() not in body.lower():
        return True

    # Look for checklist items after acceptance criteria
    return "- [ ]" not in body


def analyze_issues(issues):
    report = {
        "total": len(issues),
        "by_type": {},
        "missing_acceptance_criteria": [],
        "missing_priority": [],
        "missing_potential_subtasks": [],
        "missing_user_value": [],
    }

    for issue in issues:
        title = issue.get("title", "").strip()
        body = issue.get("body", "") or ""
        number = issue.get("number")

        issue_type = classify_issue_type(title)
        report["by_type"][issue_type] = report["by_type"].get(issue_type, 0) + 1

        if missing_acceptance_criteria(body):
            report["missing_acceptance_criteria"].append((number, title))

        if not has_section(body, "Priority"):
            report["missing_priority"].append((number, title))

        if not has_section(body, "Potential Subtasks"):
            report["missing_potential_subtasks"].append((number, title))

        if issue_type == "Feature" and not has_section(body, "User Value"):
            report["missing_user_value"].append((number, title))

    return report


def print_report(report):
    print("\n=== Agentic Product Ops: Backlog Health Report ===\n")
    print(f"Total issues analyzed: {report['total']}\n")

    print("Issue counts by type:")
    for issue_type, count in report["by_type"].items():
        print(f"  - {issue_type}: {count}")

    print("\nIssues missing acceptance criteria:")
    if report["missing_acceptance_criteria"]:
        for number, title in report["missing_acceptance_criteria"]:
            print(f"  - #{number}: {title}")
    else:
        print("  - None")

    print("\nIssues missing priority section:")
    if report["missing_priority"]:
        for number, title in report["missing_priority"]:
            print(f"  - #{number}: {title}")
    else:
        print("  - None")

    print("\nIssues missing potential subtasks section:")
    if report["missing_potential_subtasks"]:
        for number, title in report["missing_potential_subtasks"]:
            print(f"  - #{number}: {title}")
    else:
        print("  - None")

    print("\nFeature issues missing user value section:")
    if report["missing_user_value"]:
        for number, title in report["missing_user_value"]:
            print(f"  - #{number}: {title}")
    else:
        print("  - None")

    print("\n=== End Report ===\n")


def main():
    issues = fetch_issues()
    report = analyze_issues(issues)
    print_report(report)


if __name__ == "__main__":
    main()