from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from jinja2 import Environment, FileSystemLoader

from app.config import settings

jinja_env = Environment(
    loader=FileSystemLoader("app/templates")
)

def render_template(template_name:str, variables: dict)-> str:
    template=jinja_env.get_template(f"{template_name}.html")
    return template.render(**variables)

async def send_email(to: str, subject: str, template: str, variables: dict)->bool:
    try:
        html=render_template(template, variables)

        message = MIMEMultipart("alternative")
        message["From"] = settings.MAIL_FROM
        message["To"] = to
        message["Subject"] = subject
        message.attach(MIMEText(html,"html"))
        await aiosmtplib.send(message, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT, username=settings.SMTP_USER, password=settings.SMTP_PASSWORD, start_tls=True) 
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False
