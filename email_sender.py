import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "cellulardiseasemodels@gmail.com"
EMAIL_PASSWORD = "..."
TO_EMAIL = "k.h.vandersteen@umcutrecht.nl"

already_emailed_ids = set()  # Track IDs that have already been emailed

def send_email(process_id, response_data):
    """Send an email with the error details."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = f"Error Notification: Process Execution ID {process_id}"

    body = f"""
    An error has occurred.

    Process Execution ID: {process_id}
    Details: {json.dumps(response_data, indent=4)}
    """
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())

def process_response(response_json):
    """Process the API response and send emails for new errors."""
    global already_emailed_ids

    try:
        data = json.loads(response_json)
    except json.JSONDecodeError as e:
        print(f"Failed to parse response: {e}")
        return

    if not data:  # Empty response
        print("No errors found. Retrying in 5 minutes...")
        return

    for entry in data:
        process_id = entry.get("processExecutionId")
        if process_id and process_id not in already_emailed_ids:
            send_email(process_id, entry)
            already_emailed_ids.add(process_id)
            print(f"Email sent for Process Execution ID: {process_id}")
        else:
            print(f"Process Execution ID {process_id} already processed or invalid. Skipping.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python email_sender.py <response_json>")
        sys.exit(1)

    process_response(sys.argv[1])