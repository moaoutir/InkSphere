from celery import shared_task
import os
from django.core.mail import EmailMessage
from newsletter_generator.chains import Chain

chain = Chain()


@shared_task()
def process_newsletter_task(topic_blog, full_url, subject, recipients):
    html_content = chain.run(topic_blog, full_url)
    from_email = os.environ.get("EMAIL_HOST_USER")
    email = EmailMessage(subject, html_content, from_email, recipients)
    email.content_subtype = "html"
    email.send(fail_silently=False)
    print(f"Newsletter sent to {recipients} with subject: {subject}")
