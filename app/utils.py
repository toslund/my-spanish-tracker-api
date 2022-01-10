import logging, os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, PackageLoader, select_autoescape

from jose import jwt

from app.core.config import settings


def send_email(
    email_to: str,
    subject: str = "",
    html_template_name: str = "",
    txt_template_name: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    if settings.DEV_MODE:
        # Do not send live emails to real users in dev mode
        email_domain = settings.EMAILS_FROM_EMAIL.split('@')[1]
        email_local = email_to.split('@')[0]
        email_to = email_local + '@' + email_domain
    env = Environment(
        loader=PackageLoader('app'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    html_template = env.get_template(html_template_name)
    html = html_template.render(**environment)
    txt_template = env.get_template(txt_template_name)
    txt = txt_template.render(**environment)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.EMAILS_FROM_EMAIL
    message["To"] = email_to
    part1 = MIMEText(txt, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(
            settings.EMAILS_FROM_EMAIL, email_to, message.as_string()
        )


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    print(f'email dir: {Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html"}')
    print(os.getcwd())
    send_email(
        email_to=email_to,
        subject=subject,
        html_template_name="test_email.html",
        txt_template_name="test_email.txt",
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery"
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject=subject,
        html_template_name="reset_password.html",
        txt_template_name="reset_password.txt",
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for {email_to}"
    server_host = settings.SERVER_HOST
    link = f"{server_host}/confirm-email?token={token}"
    send_email(
        email_to=email_to,
        subject=subject,
        html_template_name='new_account.html',
        txt_template_name='new_account.txt',
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "valid_hours": settings.EMAIL_VERIFY_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )

def generate_confirm_email_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_VERIFY_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "email": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt

def verify_confirm_email_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
        
def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt

def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
