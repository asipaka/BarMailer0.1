import smtplib
import time
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import manage_session

from utils import (
    generate_qr_code_base64,
    fetch_logo,
    is_valid_smtp_host,
    basic_html_body,
    import_custom_template,
    load_email_list
)

VERSION = "0.1.0"

# Display script details
def display_info():
    print("*************************************************\n")
    print(f"\nBCM - Version {VERSION}\nAuthor: cr1ck3ht\n")
    print("*************************************************\n")

# Confirm campaign details
def confirm_campaign(smtp_host, smtp_user, smtp_sender_email, subject, url, email_count):
    print("\n++++++++ Campaign Summary ++++++++\n")
    print(f"SMTP Host: {smtp_host}")
    print(f"SMTP User: {smtp_user}")
    print(f"SMTP Sender: {smtp_sender_email}")
    print(f"Email Subject: {subject}")
    print(f"Phishing URL: {url}")
    print(f"Number of Emails: {email_count}")
    print("\n++++++++ *************************** ++++++++")
    confirm = input("\nProceed with this campaign? (y/n): ").strip().lower()
    return confirm == 'y'

# Send email
def send_email(smtp_host, smtp_user, smtp_pass, smtp_sender_email, recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = smtp_sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(smtp_host, 587)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_sender_email, recipient, msg.as_string())
        server.quit()
        return True, f"Email sent to {recipient}"
    except smtplib.SMTPException as e:
        return False, f"Error sending email to {recipient}: {str(e)}"

# Process emails
def process_emails(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email_list, subject, body, url):
    qr_code_data = generate_qr_code_base64(url)
    qr_code_html = f'<img src="data:image/png;base64,{qr_code_data}" alt="QR Code"/>'
    body_with_qr = body + f"<br><p>Scan the QR code below:</p>{qr_code_html}"

    for email in email_list:
        email = email.strip()
        success, message = send_email(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email, subject, body_with_qr)
        print(f"{'[OK]' if success else '[FAILED]'} {email}: {message}")
        time.sleep(2)  # Add delay between emails

# Main function
def main():
        result = manage_session()
        if result is None:
            print("Error: manage_session returned None.")
        return

        smtp_host, smtp_user, smtp_pass, smtp_sender_email, subject, url, body = result
    
  
        email_list_file = input("Email list file (CSV/TXT): ").strip()
        email_list = load_email_list(email_list_file)

        if not email_list:
            print("No valid emails found. Campaign aborted.")
            return

        # Confirm campaign details
        if not confirm_campaign(smtp_host, smtp_user, smtp_sender_email, subject, url, len(email_list),):
            print("Campaign canceled by the user.")
            return

        # Start campaign
        print("\n++++++++ Starting Campaign ++++++++")
        process_emails(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email_list, subject, body, url)

        # Check if user wants to run another campaign
        another = input("\nDo you want to run another campaign? (y/n): ").strip().lower()
        if another != 'y':
            print("Exiting BarMailer0.1 Goodbye!")
            print("\n")

if __name__ == "__main__":
    main()