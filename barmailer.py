import smtplib
import time
import sys
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

# Send email
def send_email(smtp_host, smtp_user, smtp_pass, smtp_sender_email, recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = smtp_sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    
    # Ensure the email is sent as HTML
    msg.attach(MIMEText(body, 'html'))  # Use 'html' to ensure proper rendering of HTML content

    try:
        server = smtplib.SMTP(smtp_host, 587)
        server.starttls()  # Encrypt the connection
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_sender_email, recipient, msg.as_string())  # Send email
        server.quit()
        return True, f"Email sent to {recipient}"
    except smtplib.SMTPException as e:
        return False, f"Error sending email to {recipient}: {str(e)}"

# Process emails
def process_emails(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email_list, subject, body, url):
    # Generate the QR code for the phishing URL
    qr_code_data = generate_qr_code_base64(url)  # Generate QR code for phishing URL
    
    if not qr_code_data:
        print("Error generating QR code.")
        return
    
    # Create the HTML <img> tag with the generated QR code base64 data
    qr_code_html = f'<img src="data:image/png;base64,{qr_code_data}" alt="QR Code"/>'

    # Replace the {{QR_CODE}} placeholder in the body with the actual QR code
    body_with_qr = body.replace("{{QR_CODE}}", qr_code_html)

    # Debugging: Check the body after QR code replacement
    print("Email Body with QR code:")
    print(body_with_qr)  # This helps to visually inspect the final HTML email body

    # Process each email
    for email in email_list:
        email = email.strip()

        # Generate dynamic content (e.g., username/email) for each email body
        personalized_body = body_with_qr.replace("{{USERNAME}}", email)  # Replace placeholder with email address
        
        success, message = send_email(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email, subject, personalized_body)
        print(f"{'[OK]' if success else '[FAILED]'} {email}: {message}")
        time.sleep(2)  # Add delay between emails

# Main function
def main():
    display_info()
    result = manage_session()
    if not result:
        print("++++++++++ No Previous sessions ++++++++++\n")
        return  # Exit if no configuration was provided

    # Unpack session details
    smtp_host, smtp_user, smtp_pass, smtp_sender_email, subject, url, body = result

    # Prompt for the email list file
    email_list_file = input("Email list file (CSV/TXT): ").strip()
    email_list = load_email_list(email_list_file)

    if not email_list:
        print("No valid emails found. Campaign aborted.")
        return

    # Confirm campaign details
    if not confirm_campaign(smtp_host, smtp_user, smtp_sender_email, subject, url, len(email_list)):
        print("Campaign canceled by the user.")
        return

    # Start campaign
    print("\n++++++++ Starting Campaign ++++++++")
    process_emails(smtp_host, smtp_user, smtp_pass, smtp_sender_email, email_list, subject, body, url)

    # Check if the user wants to run another campaign
    another = input("\nDo you want to run another campaign? (y/n): ").strip().lower()
    print("*************************************************\n")
    if another != 'y':
        print("Exiting BarMailer0.1 Goodbye!")
        print("*************************************************\n")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
