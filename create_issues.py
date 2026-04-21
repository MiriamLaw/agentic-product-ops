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

ISSUES = [
    {
        "title": "Feature: View Student Assignment Completion By Course",
        "body": """## Summary
As an instructor, I need visibility into student assignment completion across my courses.

## Type
Feature

## User Value
Helps instructors identify students who may be falling behind.

## Acceptance Criteria
- [ ] View assignment completion by course
- [ ] Completion data is accurate and current
- [ ] Results are easy to scan by student

## Potential Subtasks
- Frontend course completion view
- Backend API for assignment completion
- QA validation

## Priority
High
""",
    },
    {
        "title": "Feature: View Upcoming Assignment Due Dates In One Place",
        "body": """## Summary
As a student, I need a central place to view upcoming due dates across courses.

## Type
Feature

## User Value
Improves planning and assignment completion.

## Acceptance Criteria
- [ ] Upcoming due dates display in one view
- [ ] Dates are sorted correctly
- [ ] Past due assignments are visually distinct

## Potential Subtasks
- Frontend due date component
- Backend due date aggregation
- QA testing

## Priority
High
""",
    },
    {
        "title": "Bug: Fix Duplicate Assignment Reminder Notifications",
        "body": """## Summary
Some users receive duplicate reminder notifications for the same assignment.

## Type
Bug

## User Value
Reduces confusion and notification fatigue.

## Acceptance Criteria
- [ ] Duplicate notifications no longer occur
- [ ] Existing reminder workflows still function correctly
- [ ] Regression testing completed

## Potential Subtasks
- Backend notification logic review
- QA regression testing

## Priority
High
""",
    },
    {
        "title": "Feature: Filter Student Progress Reports By Date Range",
        "body": """## Summary
As an admin, I need more flexible date filtering when reviewing student progress reports.

## Type
Feature

## User Value
Improves reporting accuracy and saves time.

## Acceptance Criteria
- [ ] Start and end dates can be selected
- [ ] Reports return correct records for the chosen range
- [ ] Invalid date ranges are prevented

## Potential Subtasks
- Frontend date range picker
- Backend query updates
- QA edge case testing

## Priority
Medium
""",
    },
    {
        "title": "Feature: Identify Students With Low Engagement",
        "body": """## Summary
As an advisor, I need a way to identify students with low engagement activity.

## Type
Feature

## User Value
Helps advisors intervene earlier with at-risk students.

## Acceptance Criteria
- [ ] Low-engagement students can be viewed in a report or list
- [ ] Engagement threshold is applied correctly
- [ ] Results are current and accurate

## Potential Subtasks
- Backend engagement calculation
- Frontend advisor view
- QA validation

## Priority
High
""",
    },
    {
        "title": "Bug: Improve Load Time On Course Analytics Dashboard",
        "body": """## Summary
Course analytics dashboard is loading too slowly for some users.

## Type
Bug

## User Value
Improves usability and trust in the platform.

## Acceptance Criteria
- [ ] Dashboard load time improves
- [ ] Analytics data remains accurate
- [ ] Performance verified in testing

## Potential Subtasks
- Backend query optimization
- Frontend performance review
- QA testing

## Priority
High
""",
    },
    {
        "title": "Feature: Export Course Analytics To CSV",
        "body": """## Summary
As an instructor, I need to export course analytics for offline review and sharing.

## Type
Feature

## User Value
Supports reporting and collaboration outside the platform.

## Acceptance Criteria
- [ ] Export option is available
- [ ] CSV downloads successfully
- [ ] Exported data matches visible analytics

## Potential Subtasks
- Frontend export button
- Backend CSV generation
- QA validation

## Priority
Medium
""",
    },
    {
        "title": "Feature: Reset Password Without Contacting Support",
        "body": """## Summary
As a student, I need a self-service password reset workflow.

## Type
Feature

## User Value
Improves access and reduces support burden.

## Acceptance Criteria
- [ ] Password reset can be initiated from login
- [ ] Reset email is sent successfully
- [ ] Users can set a new valid password

## Potential Subtasks
- Frontend password reset screen
- Backend password reset endpoint
- QA testing

## Priority
High
""",
    },
    {
        "title": "Bug: Fix Incorrect Counts In Student Engagement Summary",
        "body": """## Summary
Student engagement summary is showing incorrect totals in some cases.

## Type
Bug

## User Value
Prevents decisions based on inaccurate data.

## Acceptance Criteria
- [ ] Correct totals are displayed
- [ ] Known edge cases are covered
- [ ] QA verifies expected values

## Potential Subtasks
- Backend aggregation review
- QA data validation

## Priority
High
""",
    },
    {
        "title": "Feature: Search Users By Name Or Email",
        "body": """## Summary
As an admin, I need quicker access to user records.

## Type
Feature

## User Value
Improves support efficiency.

## Acceptance Criteria
- [ ] Search by full or partial name
- [ ] Search by email
- [ ] Results load within acceptable time

## Potential Subtasks
- Frontend search UI
- Backend query/API
- QA testing

## Priority
Medium
""",
    },
    {
        "title": "Feature: Post Course Announcements",
        "body": """## Summary
As an instructor, I need a way to share announcements with students in a course.

## Type
Feature

## User Value
Improves communication and course coordination.

## Acceptance Criteria
- [ ] Instructors can create announcements
- [ ] Students can view announcements
- [ ] Announcement content saves correctly

## Potential Subtasks
- Frontend announcement UI
- Backend announcement model/API
- QA testing

## Priority
Medium
""",
    },
    {
        "title": "Bug: Fix Assignment Status Not Updating After Submission",
        "body": """## Summary
Some assignments continue showing as incomplete after successful submission.

## Type
Bug

## User Value
Prevents confusion and inaccurate progress tracking.

## Acceptance Criteria
- [ ] Assignment status updates after submission
- [ ] No false incomplete states remain
- [ ] Regression testing completed

## Potential Subtasks
- Backend submission/status logic
- QA validation

## Priority
High
""",
    },
    {
        "title": "Feature: View Course Completion Trends Over Time",
        "body": """## Summary
As a program lead, I need visibility into course completion trends over time.

## Type
Feature

## User Value
Supports data-informed program decisions.

## Acceptance Criteria
- [ ] Trend view displays over time
- [ ] Completion data is accurate
- [ ] Filters apply correctly

## Potential Subtasks
- Frontend visualization
- Backend trend calculation
- QA testing

## Priority
Medium
""",
    },
    {
        "title": "Feature: View Unread Notifications Separately From Read Notifications",
        "body": """## Summary
As a student, I need better visibility into unread notifications.

## Type
Feature

## User Value
Improves clarity and reduces missed messages.

## Acceptance Criteria
- [ ] Unread notifications are visually distinct
- [ ] Read/unread state updates correctly
- [ ] Filtering works as expected

## Potential Subtasks
- Frontend notification filter
- Backend notification state support
- QA testing

## Priority
Medium
""",
    },
    {
        "title": "Bug: Fix Missing Error Message When Report Export Fails",
        "body": """## Summary
When report export fails, users do not see a clear error message.

## Type
Bug

## User Value
Improves usability and troubleshooting.

## Acceptance Criteria
- [ ] Error message displays on export failure
- [ ] Message is user-friendly
- [ ] Success path still works correctly

## Potential Subtasks
- Frontend error handling
- QA validation

## Priority
Medium
""",
    },
    {
        "title": "Feature: Assign User Roles During Account Setup",
        "body": """## Summary
As an admin, I need to assign roles when creating or managing accounts.

## Type
Feature

## User Value
Improves access control and onboarding.

## Acceptance Criteria
- [ ] Role can be selected during setup
- [ ] Role is saved correctly
- [ ] Permission behavior reflects assigned role

## Potential Subtasks
- Frontend admin form updates
- Backend role assignment logic
- QA permission testing

## Priority
Medium
""",
    },
    {
        "title": "Bug: Fix Inactive Users Appearing In Active User Reports",
        "body": """## Summary
Inactive users are incorrectly appearing in active user reporting.

## Type
Bug

## User Value
Improves reporting accuracy.

## Acceptance Criteria
- [ ] Inactive users are excluded appropriately
- [ ] Existing active user counts remain correct
- [ ] QA validates report logic

## Potential Subtasks
- Backend reporting query review
- QA validation

## Priority
Medium
""",
    },
    {
        "title": "Feature: Filter Student Lists By Engagement Status",
        "body": """## Summary
As an instructor, I need to quickly identify students by engagement level.

## Type
Feature

## User Value
Supports earlier intervention and more targeted follow-up.

## Acceptance Criteria
- [ ] Engagement status filter is available
- [ ] Filter results are accurate
- [ ] UI clearly communicates selected status

## Potential Subtasks
- Frontend filtering UI
- Backend filter support
- QA testing

## Priority
Medium
""",
    },
    {
        "title": "Bug: Fix Unexpected Logout During Active Sessions",
        "body": """## Summary
Users are being logged out unexpectedly during active sessions.

## Type
Bug

## User Value
Improves reliability and user trust.

## Acceptance Criteria
- [ ] Active users remain logged in as expected
- [ ] Unexpected logout issue no longer reproduces
- [ ] Session handling verified in testing

## Potential Subtasks
- Backend session review
- QA testing

## Priority
High
""",
    },
    {
        "title": "Feature: View Recent User Account Activity",
        "body": """## Summary
As an admin, I need visibility into recent account actions for support and auditing.

## Type
Feature

## User Value
Improves support response and account oversight.

## Acceptance Criteria
- [ ] Recent account activity is visible
- [ ] Activity list is accurate
- [ ] Entries are ordered by most recent first

## Potential Subtasks
- Frontend activity view
- Backend activity endpoint
- QA testing

## Priority
Low
""",
    },
]


def create_issue(issue: dict) -> None:
    response = requests.post(API_URL, headers=HEADERS, json=issue, timeout=30)

    if response.status_code == 201:
        created = response.json()
        print(f"Created issue #{created['number']}: {created['title']}")
    else:
        print(f"Failed to create issue: {issue['title']}")
        print(f"Status: {response.status_code}")
        print(response.text)
        print("-" * 60)


def main() -> None:
    print(f"Creating issues in {GITHUB_OWNER}/{GITHUB_REPO}...")
    for issue in ISSUES:
        create_issue(issue)
    print("Done.")


if __name__ == "__main__":
    main()