import csv
import os
import base64
import qrcode
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io
import sys

DEFAULT_SMTP_HOST = "smtp.mailtrap.io"
DEFAULT_SMTP_USER = "your_mailtrap_user"
DEFAULT_SMTP_PASS = "your_mailtrap_password"
DEFAULT_SENDER_EMAIL = "test@bcm.com"

def get_smtp_host():
    """Function to get the SMTP host address."""
    # Placeholder function; replace with your actual method to get SMTP host
    return input("Enter SMTP host (e.g., smtp.gmail.com): ").strip()

def basic_html_body():
    """Function to return the default email template."""
    # This is where you define the basic HTML template for your phishing email
    return "<html><body><h1>Default Phishing Body</h1></body></html>"

def import_custom_template():
    """Function to load a custom email template."""
    # Replace with logic to load your custom HTML template
    template_path = input("Enter the path to your custom template: ").strip()
    with open(template_path, 'r') as template_file:
        return template_file.read()

def manage_session():
    """Manage the session for new or continued campaign."""
    session_file = 'previous_config.txt'

    # Check if there's a previous configuration session
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            previous_config = f.read().splitlines()

        # Show the previous configuration to the user
        print("\n++++++ Previous Configuration ++++++")
        print("\n".join(previous_config))

        # Ask if the user wants to continue with the previous session
        continue_session = input("\nDo you want to use the previous configuration (y/n)?: ").strip().lower()

        if continue_session == 'y':
            print("\n++++++++ Continuing with Previous Config ++++++++\n")
            try:
                smtp_host = previous_config[0]
                smtp_user = previous_config[1]
                smtp_pass = previous_config[2]
                smtp_sender_email = previous_config[3]
                subject = previous_config[4]
                url = previous_config[5]
                body = previous_config[6]
                return smtp_host, smtp_user, smtp_pass, smtp_sender_email, subject, url, body
            except IndexError:
                print("Error: Configuration file is corrupted or incomplete.")
                print("Starting a new session...")
        else:
            print("\n++++++++ Starting a New Session ++++++++\n")
    else:
        print("\n------------ No Previous Sessions ------------\n")

    # Prompt user for new session details
    smtp_host = input(f"SMTP Host (default: smtp.mailtrap.io): ").strip() or "smtp.mailtrap.io"
    smtp_user = input(f"SMTP User (default: your_mailtrap_user): ").strip() or "your_mailtrap_user"
    smtp_pass = input(f"SMTP Password (default: your_mailtrap_password): ").strip() or "your_mailtrap_password"
    smtp_sender_email = input(f"SMTP Sender Email (default: test@bcm.com): ").strip() or "test@bcm.com"
    subject = input("Email Subject: ").strip()
    url = input("Phishing URL: ").strip()

    print("\n")

    use_default = input("Do you want to use the default email template for testing? (y/n): ").strip().lower()
    if use_default == 'y':
        body = basic_html_body()
    elif use_default == 'n':
        filepath = input("Enter the path to your custom template file: ")
        body = import_custom_template(filepath)  # Pass the filepath argument
    else:
        print("Invalid input. Exiting the program.")
        sys.exit(1)

    # Save the new configuration to the session file
    with open(session_file, 'w') as f:
        f.write(f"{smtp_host}\n{smtp_user}\n{smtp_pass}\n{smtp_sender_email}\n{subject}\n{url}\n{body}")

    print("\n++++++ New Session Config Saved ++++++\n")
    return smtp_host, smtp_user, smtp_pass, smtp_sender_email, subject, url, body

# Generate QR code in base64 format
def generate_qr_code_base64(data):
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return ""

# Fetch logo from a local or remote source (not used directly in this version but included for extension)
def fetch_logo(path):
    if os.path.exists(path):
        with open(path, 'rb') as logo_file:
            return base64.b64encode(logo_file.read()).decode('utf-8')
    return None


# Validate SMTP host format
def is_valid_smtp_host(host):
    return '.' in host and len(host) > 5  # Basic validation for hostname structure

# **New Function**: Generate email body by replacing placeholders with actual data (username, QR code, URL)
def generate_email_body(username, qr_code_url, verification_url):
    try:
        # You can either use a hardcoded template or dynamically load it from a file
        email_body = basic_html_body()  # You can replace this with import_custom_template if needed
        
        # Replace placeholders with actual dynamic data
        email_body = email_body.replace('{{USERNAME}}', username)
        email_body = email_body.replace('{{QR_CODE}}', qr_code_url)
        email_body = email_body.replace('{{URL}}', verification_url)

        return email_body
    except Exception as e:
        print(f"Error in generating email body: {e}")
        return None

# Basic HTML body for email
def basic_html_body():
    return """<html>
        <body>
            <h1>Action Required</h1>
            <p>Hello {{USERNAME}},</p>
            <p>Please scan the QR code or click the link below to verify your details:</p>
            <p><img src="data:image/png;base64,{{QR_CODE}}" alt="QR Code"></p>
            <a href="{{URL}}">Verify Now</a>
        </body>
    </html>"""

# Import a custom HTML template
def import_custom_template(filepath):
    if not os.path.exists(filepath):
        print(f"Template file not found: {filepath}")
        return basic_html_body()  # Fallback to default template
    with open(filepath, 'r') as template_file:
        return template_file.read()

# Load email list from CSV or TXT file
def load_email_list(filepath):
    emails = []
    try:
        with open(filepath, 'r') as file:
            if filepath.endswith('.csv'):
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Check for non-empty rows
                        emails.append(row[0].strip())
            elif filepath.endswith('.txt'):
                emails = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error loading email list: {str(e)}")
    return emails