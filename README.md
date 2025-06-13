# Automated Email Reminder System

This repository contains an automated email reminder system that reads recipient data and messages from a Google Spreadsheet and sends out scheduled email reminders. Originally built during my internship as a **Security Assurance Intern** using **Google Apps Script**, this system has been re-implemented using **Python**, **GitHub Actions**, and the **Google Sheets API** for broader automation capabilities in CI/CD environments.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [File Structure](#file-structure)  
- [How It Works](#how-it-works)  
- [Setup & Configuration](#setup--configuration)  
- [GitHub Actions Workflow](#github-actions-workflow)  

---

## Overview

This tool automates the process of sending scheduled email reminders using data from a Google Spreadsheet.  
It fetches recipient details and messages, and then sends emails via Gmail SMTP. The automation runs twice a week using GitHub Actions, with all sensitive information securely managed through GitHub Secrets.

---

## Features

- Sends email reminders on a fixed weekly schedule  
- Reads recipient information and message content from Google Sheets  
- Sends emails via Gmail using SMTP  
- Configurable using environment variables and GitHub Secrets  
- Fully automated using GitHub Actions

---

## Tech Stack

- Python 3.x  
- Google Sheets API  
- `smtplib` and `email.mime` (for sending emails)  
- `oauth2client` (for Google API authentication)  
- GitHub Actions (CI/CD automation)  
- GitHub Secrets (for managing credentials securely)

---

## File Structure

```bash
.
├── .github/
│   └── workflows/
│       └── email_reminder.yml    # GitHub Actions workflow definition
├── data
│   └── issues_sample.csv         # This is a sample CSV file to show the expected structure of issue data
├── main.py                       # Python script to send emails
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## How It Works

1. GitHub Actions is triggered automatically on a schedule (every Tuesday and Thursday at 10:00 AM WIB).  
2. The credentials file is reconstructed from the base64-encoded GitHub Secret.  
3. The Python script authenticates with the Google Sheets API using a service account.  
4. Recipient data and messages are fetched from the Google Spreadsheet.  
5. Emails are sent via Gmail SMTP using the provided credentials.  

---

## Setup & Configuration

### Prerequisites

- A Google Service Account with access to the target spreadsheet  
- A Gmail account with an App Password enabled (required if 2FA is active)  
- A GitHub repository to host the workflow and Python scripts  

### Configuration Steps

1. Create a Google Cloud project and enable the Google Sheets API.  
2. Generate a service account and download the credentials JSON file.  
3. Encode the credentials file using base64 and store it as a GitHub Secret.  
4. Add other necessary secrets to GitHub (e.g., Gmail credentials, spreadsheet ID).  
5. Configure the GitHub Actions workflow to run on your desired schedule.  

---

## GitHub Actions Workflow

The automation runs based on the following cron schedule:

```yaml
on:
  schedule:
    - cron: '0 3 * * 2,4'  # 03:00 UTC = 10:00 AM (WIB) every Tuesday and Thursday
```

This schedule will trigger the email reminder system twice a week.

---

Thank you for reading!
