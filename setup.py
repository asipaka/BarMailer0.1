from setuptools import setup, find_packages

setup(
    name="BarMailer",
    version="0.1.0",
    packages=find_packages(where="."),  # Look in the current directory for packages
    include_package_data=True,
    install_requires=[
        "qrcode",
        "pillow",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "barmailer=barmailer:main",  # The entry point for your package
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
    python_requires='>=3.6',  # Python compatibility
)