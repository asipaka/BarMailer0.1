import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import manage_session, generate_qr_code_base64, load_email_list, generate_email_body

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

# Verify SMTP credentials
def verify_smtp_credentials(smtp_host, smtp_user, smtp_pass):
    try:
        print("\nVerifying SMTP credentials...")
        server = smtplib.SMTP(smtp_host, 587)
        server.starttls()  # Start encrypted connection
        server.login(smtp_user, smtp_pass)
        server.quit()
        print("[OK] SMTP credentials are valid.")
        return True
    except smtplib.SMTPAuthenticationError:
        print("[FAILED] Authentication failed. Please check your username and password.")
    except smtplib.SMTPConnectError:
        print("[FAILED] Unable to connect to the SMTP server. Please check the host address.")
    except Exception as e:
        print(f"[FAILED] An error occurred: {str(e)}")
    return False

# Process emails
def process_emails(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email_list, subject, body, url):
    qr_code_data = generate_qr_code_base64(url)
    if not qr_code_data:
        print("Error generating QR code.")
        return
    
    qr_code_html = f'<img src="data:image/png;base64,{qr_code_data}" alt="QR Code" style="width:150px;height:150px;"/>'
    body_with_qr = body.replace("{{QR_CODE}}", qr_code_html)

    for email in email_list:
        email = email.strip()
        personalized_body = body_with_qr.replace("{{USERNAME}}", email)
        success, message = send_email(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email, subject, personalized_body)
        print(f"{'[OK]' if success else '[FAILED]'} {email}: {message}")
        time.sleep(2)

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

# Main function
def main():
    while True:
        display_info()

        result = None
        while not result:
            result = manage_session()
            if not result:
                print("++++++++++ No Previous sessions ++++++++++")
                retry = input("\nDo you want to configure a new session? (y/n): ").strip().lower()
                if retry != 'y':
                    print("Exiting program. Goodbye!")
                    return

        smtp_host, smtp_user, smtp_pass, smtp_sender_email, subject, url, body = result

        # Validate SMTP credentials only if they haven't already been verified
        if not verify_smtp_credentials(smtp_host, smtp_user, smtp_pass):
            print("Invalid SMTP credentials. Please reconfigure.")
            continue

        email_list_file = input("Email list file (CSV/TXT): ").strip()
        email_list = load_email_list(email_list_file)

        if not email_list:
            print("No valid emails found. Campaign aborted.")
            continue

        if not confirm_campaign(smtp_host, smtp_user, smtp_sender_email, subject, url, len(email_list)):
            print("Campaign canceled by the user.")
            continue

        print("\n++++++++ Starting Campaign ++++++++")
        process_emails(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email_list, subject, body, url)
        print("\n+++++++++++++++++++++++++++++++++++")

        print("\n*************************************************")
        another = input("\nDo you want to run another campaign? (y/n): ").strip().lower()
        print("\n*************************************************")
        if another != 'y':
            print("Exiting BarMailer0.1 Goodbye!")
            print("*************************************************\n")
            break

# Run the main function when the script is executed
if __name__ == "__main__":
    main()