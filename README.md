**BarMailer (BcM)**
BarMailer is a QR-enabled email automation tool designed for streamlined bulk email campaigns. Whether you're sending newsletters, marketing emails, or custom messages, BarMailer ensures simplicity and functionality with built-in QR code generation.

**Features**

**QR Code Embedding**: Automatically embed personalized QR codes into emails for added interactivity.
**Customizable Templates**: Use a default email template or import your own HTML templates.
**Session Continuity**: Save and reuse configurations from previous campaigns.
**Simple Workflow**: Input settings once and focus on your campaign, without repeated setups.
**Error Handling**: Alerts for any misconfigurations or delivery issues.

**Installation**
Follow these steps to install and run BarMailer on your system:

**Pre-requisites**
Ensure you have Python 3.6+ installed on your machine.
Verify you have pip installed (comes bundled with Python).
Clone or download this repository.

**Installation Steps**
Navigate to the project folder:
**bash**
cd BarMailer
Install the tool using the setup.py script:
**bash**
python setup.py install
This will install all dependencies and set up the tool for use.
**Running BarMailer**
After installation, you can start the tool directly from your terminal using the command:
**bash**
bar-mailer


**First-Time Setup**
SMTP Configuration:

Enter the SMTP host (e.g., smtp.gmail.com).
Provide your SMTP username and password.

**Email Settings:**
Input the subject of your email.
Provide the URL for generating QR codes.
Choose between the default email template or importing a custom HTML template.

**Recipient List:**
Prepare a .txt file containing the email addresses of recipients (one per line).
When prompted, provide the path to this file.

**Review Configuration:**
The tool will display the settings for review. Confirm to start the campaign.

**Saving and Resuming Campaigns**
BarMailer saves your previous configuration automatically:
On subsequent runs, you'll be prompted to use the saved settings or start fresh.

**Development and Customization**
BarMailer is extensible and allows for adding features such as license key validation, advanced templating, and more.
You can modify scripts under the src folder to adapt the tool to specific needs.

**Dependencies**
The following libraries are required and installed during setup:
qrcode
pillow
requests

**FAQ**
**1. How do I prepare the recipient email list?**
Create a plain .txt file with one email address per line.
**Example:**
example1@gmail.com  
example2@gmail.com  
example3@gmail.com 

**2. What if the SMTP server rejects my credentials?**
Ensure your SMTP settings are correct.
For Gmail, enable "Allow less secure apps" in your account settings, or generate an app-specific password.

**3. Can I use my own HTML template?**
Yes, you can import your HTML template by selecting the custom template option during setup.

**4. Can I include attachments?**
This version doesn't currently support attachments, but you can modify the send_email function in the src/utils.py file to add this feature.

**Contributing**
Contributions are welcome! Fork the repository, make changes, and submit a pull request.

**License**
BarMailer is licensed under the MIT License.

