# Open Issues Automation Reminder

## What’s This About?

This project helps you keep track of important open issues by automatically sending reminder emails. It makes sure nothing important is forgotten and everyone stays updated on what needs attention!

Built with Python and designed to run smoothly on Linux, it uses the GitHub API plus cron scheduling to make sure you stay on top of your repo’s open tasks!

## Why Did I Build This?

Back when I was interning as part of a Security Assurance team, I created an automation reminder using Google Apps Script to track important security findings from User Access Reviews and Management processes across various apps. It helped the teams responsible stay in the loop about outstanding issues.

Fast forward to now, I wanted a more robust, flexible, and scalable version — so here it is, rewritten in Python to run on Linux! It’s perfect for anyone who wants to bring some automation magic to their DevOps workflow.

## Cool Features

- Automatically scans your GitHub repositories for open issues.
- Sends reminder emails to relevant stakeholders.
- Supports filtering and formatting of issues in the email.
- Runs seamlessly on Linux using cron jobs for scheduling.
- Uses Google Sheets for tracking and collaboration.
- Easy to set up, configure, and customize to your workflow.

## How to Use It

### Prerequisites

- Python 3.6 or higher
- Access to a Google Sheets document for issue tracking
- Google Cloud Service Account with Sheets API enabled (`credentials.json`)
- Gmail account with an app password for sending emails
- GitHub personal access token (if using GitHub API integration)

---

Thank you for reading! 🙏
