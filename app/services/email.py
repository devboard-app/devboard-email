import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from app.config import settings
from app.exceptions import (
    EmailDeliveryException,
    RecipientRefusedException,
    TemplateNotFoundException,
)

logger = logging.getLogger(__name__)

jinja_env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

def render_template(template_name:str, variables: dict)-> str:
    try:
        template=jinja_env.get_template(f"{template_name}.html")
    except TemplateNotFound:
        logger.warning(f"Unknown email template: {template_name}")
        raise TemplateNotFoundException()
    return template.render(**variables, app_url=settings.APP_URL)

def build_message(to: str, subject: str, html: str) -> MIMEMultipart:
    message = MIMEMultipart("alternative")
    message["From"] = settings.MAIL_FROM
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(html, "html"))
    return message

async def send_email(to: str, subject: str, template: str, variables: dict) -> None:
    html=render_template(template, variables)
    message = build_message(to, subject, html)
    try:
        await aiosmtplib.send(message, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT, username=settings.SMTP_USER, password=settings.SMTP_PASSWORD, start_tls=True) 
    except aiosmtplib.SMTPRecipientsRefused:
        logger.warning(f"Recipients refused: {to}")
        raise RecipientRefusedException()
    except aiosmtplib.SMTPException:
        logger.error(f"Failed to send email to {to}")
        raise EmailDeliveryException()
