import smtplib
import gspread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT"))
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")

COL_ID = "ID Issue"
COL_APP = "Application"
COL_SO = "Service Owner"
COL_SO_EMAIL = "Service Owner Email"
COL_TYPE = "Type"
COL_DESC = "Issue Description"
COL_STATUS = "Status"

def get_log_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def load_spreadsheet_data():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(credentials)
        sheet = client.open(SPREADSHEET_NAME).sheet1
        data = sheet.get_all_records()
        return data
    except Exception as e:
        print(f"{get_log_timestamp()} | Spreadsheet error: {e}")
        return None

def filter_open_issues(data):
    return [row for row in data if row.get(COL_STATUS) == "Open"]

def extract_recipient_emails(open_issues):
    emails = {row.get(COL_SO_EMAIL) for row in open_issues if row.get(COL_SO_EMAIL)}
    return list(emails)

def build_email_html(issues):
    rows_html = ""
    for row in issues:
        rows_html += f"""
        <tr>
            <td>{row.get(COL_ID)}</td>
            <td>{row.get(COL_APP)}</td>
            <td>{row.get(COL_SO)}</td>
            <td>{row.get(COL_SO_EMAIL)}</td>
            <td>{row.get(COL_TYPE)}</td>
            <td>{row.get(COL_DESC)}</td>
            <td>{row.get(COL_STATUS)}</td>
        </tr>
        """
    html = f"""
    <html>
    <head>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #333;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #ddd;
        }}
        p {{
            font-family: Arial, sans-serif;
        }}
    </style>
    </head>
    <body>
        <p>Dear Team,</p>
        <p>This is a friendly reminder regarding the following issues that are still <strong>Open</strong>. Please kindly review and take necessary action.</p>
        <table>
            <thead>
                <tr>
                    <th>ID Issue</th>
                    <th>Application</th>
                    <th>Service Owner</th>
                    <th>Service Owner Email</th>
                    <th>Type</th>
                    <th>Issue Description</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        <p>Please address these items at your earliest convenience to ensure timely resolution.<br>
        Should you have any questions or require further clarification, feel free to reach out.<br><br>
        <strong>Best regards,<br>Security Assurance</strong></p>
    </body>
    </html>
    """
    return html

def build_email_text(issues):
    lines = ["Dear Team,", "", "This is a kind reminder regarding the following open issues that are still pending resolution. Kindly review and take necessary action:", ""]
    header = f"{COL_ID}\t{COL_APP}\t{COL_SO}\t{COL_SO_EMAIL}\t{COL_TYPE}\t{COL_DESC}\t{COL_STATUS}"
    lines.append(header)
    for row in issues:
        line = f"{row.get(COL_ID)}\t{row.get(COL_APP)}\t{row.get(COL_SO)}\t{row.get(COL_SO_EMAIL)}\t{row.get(COL_TYPE)}\t{row.get(COL_DESC)}\t{row.get(COL_STATUS)}"
        lines.append(line)
    lines.append("")
    lines.append("Please address these items at your earliest convenience to ensure timely resolution.")
    lines.append("Should you have any questions or require further clarification, feel free to reach out.")
    lines.append("")
    lines.append("Best regards,")
    lines.append("Security Assurance")
    return "\n".join(lines)

def send_email(recipients, subject, html_content, text_content):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_SENDER
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, recipients, msg.as_string())
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")

def main():
    try:
        data = load_spreadsheet_data()
        if data is None:
            print(f"{get_log_timestamp()} | Spreadsheet error | Skipped")
            return

        open_issues = filter_open_issues(data)
        if not open_issues:
            print(f"{get_log_timestamp()} | 0 open issues | No email sent")
            return

        recipients = extract_recipient_emails(open_issues)
        if not recipients:
            print(f"{get_log_timestamp()} | {len(open_issues)} open issues | 0 recipients | No email sent")
            return

        email_html = build_email_html(open_issues)
        email_text = build_email_text(open_issues)

        send_email(recipients, "[Reminder] Outstanding Open Issues – Action Needed", email_html, email_text)
        print(f"{get_log_timestamp()} | {len(open_issues)} open issues | {len(recipients)} recipients | Email sent")

    except Exception as e:
        print(f"{get_log_timestamp()} | Script error: {e} | Skipped")

if __name__ == "__main__":
    main()
