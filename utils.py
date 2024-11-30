import csv
import os
import base64
import qrcode
import requests
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io
import sys

DEFAULT_SMTP_HOST = "smtp.mailtrap.io"
DEFAULT_SMTP_USER = "your_mailtrap_user"
DEFAULT_SMTP_PASS = "your_mailtrap_password"
DEFAULT_SENDER_EMAIL = "test@bcm.com"

# Function to generate and save a QR code as a file
def generate_qr_code_file(url, output_file="qr_code.png"):
    try:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_file)  # Save the QR code as a file
        return output_file  # Return the saved file path
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None

# Function to upload the QR code to Imgur and get a public link
def upload_qr_code_to_imgur(file_path):
    try:
        client_id = "a607b86c0481968"  # Replace with your Imgur client ID
        headers = {"Authorization": f"Client-ID {client_id}"}
        with open(file_path, "rb") as f:
            response = requests.post(
                "https://api.imgur.com/3/image",
                headers=headers,
                files={"image": f}
            )
        if response.status_code == 200:
            return response.json()["data"]["link"]  # Return the public URL
        else:
            print(f"Error uploading image: {response.json()}")
            return None
    except Exception as e:
        print(f"Error uploading QR code: {e}")
        return None

# Generate email body by replacing placeholders with actual data
def generate_email_body(username, qr_code_url, verification_url):
    try:
        email_body = basic_html_body()
        
        # Replace placeholders with actual data
        email_body = email_body.replace('{{USERNAME}}', username)
        email_body = email_body.replace('{{QR_CODE}}', qr_code_url)
        email_body = email_body.replace('{{URL}}', verification_url)

        return email_body
    except Exception as e:
        print(f"Error in generating email body: {e}")
        return None

# Default HTML email template
def basic_html_body():
    return """<html>
        <body>
            <h1>Action Required</h1>
            <p>Hello {{USERNAME}},</p>
            <p>Please scan the QR code or click the link below to verify your details:</p>
            <p><img src="{{QR_CODE}}" alt="QR Code"></p>
            <a href="{{URL}}">Verify Now</a>
        </body>
    </html>"""

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