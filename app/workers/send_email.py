import logging
import json
import asyncio
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from jinja2 import Environment, FileSystemLoader

from app.core.celery_conf import celery_app
from app.core.settings import settings


# Logger
logger = logging.getLogger(__name__)


@celery_app.task(
    acks_late=True,
)
def send_email(
    status: str,
    client_email: str,
    advisor_email: str,
    products: list[dict],
    order_id: int,
):
    """
    Main task to notify when a process has failed
    """
    try:
        asyncio.run(send_message(
            status=status,
            client_email=client_email,
            advisor_email=advisor_email,
            products=products,
            order_id=order_id,
        ))

    except Exception as e:
        return {"status": "error", "message": str(e)}
    

async def send_message(
    status: str,
    client_email: str,
    advisor_email: str,
    products: list[dict],
    order_id: int,
):
    env = Environment(loader=FileSystemLoader('app/workers/templates'))
    template = env.get_template('email_template.html')
    html_content = template.render(
        status=status,
        client_email=client_email,
        advisor_email=advisor_email,
        products=products,
        order_id=order_id,
    )

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email("santiago.ortiz@orquestia.io")
    to_email = To(client_email)
    subject = f"Order {order_id} status update"
    content = Content("text/html", html_content)
    mail = Mail(from_email, to_email, subject, content)

    mail_json = mail.get()

    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
    
    return {"status": "success", "message": "Message sent successfully"}

    
