from setuptools import setup, find_packages

setup(
    name="BarMailer",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "qrcode",  # For generating QR codes
        "pillow",  # For image handling
        "requests",  # For making HTTP requests
    ],
    entry_points={
        "console_scripts": [
            "bar-mailer=src.bar_mailer:main",  # Entry point for your main script
        ],
    },
    author="cr1ck3ht",
    description="BarMailer - A QR-enabled email automation tool.",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Ensures Python version compatibility
)
