# BarMailer

**BarMailer (BcM)** is a versatile email campaign automation tool with QR code integration. Ideal for secure communication, it supports SMTP configuration, email templates, and campaign tracking.

## Features

- SMTP configuration
- Email campaign management
- QR code integration
- Template support
- Custom email lists

## Installation

```bash

pip install -r requirements.txt

## usage 
python src/bar_mailer.py
## activation [activate before your first use]
python src/activation.py

-----------------------------------------------------------------------------------------------


### **b. `INSTALL.md`**

```markdown
# Installation Guide for BCM Mailer

Follow these steps to set up BCM Mailer:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/BCM_Mailer.git
    cd BCM_Mailer
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Activate the tool:
    ```bash
    python src/activation.py
    ```

4. Configure your SMTP settings in `config/default_config.json`:
    ```json
    {
        "smtp_host": "smtp.mailtrap.io",
        "smtp_user": "your_username",
        "smtp_pass": "your_password",
        "default_sender_email": "test@bcm.com"
    }
    ```

5. Start sending emails:
    ```bash
    python src/bcm_mailer.py
    ```
