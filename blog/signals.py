from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.core.mail import EmailMessage


from .models import Post

from newsletter_generator.chains import Chain
from dotenv import load_dotenv
import os

load_dotenv(".env.local")
chain = Chain()


@receiver(post_save, sender=Post)
def create_profile(sender, instance, created, **kwargs):
    if created:
        domain = os.environ.get("domain")
        post_url = reverse("post-detail", kwargs={"pk": instance.pk})
        full_url = domain.rstrip("/") + post_url
        topic_blog = (
            instance.title + " " + instance.content + "\n blog url: " + full_url
        )
        html_content = chain.run(topic_blog, full_url)

        subject = f"Ink Sphere: {instance.title} by {instance.author.username}"
        from_email = os.environ.get("EMAIL_HOST_USER")
        recipients = [sub.email for sub in instance.author.profile.subscribers.all()]
        print(recipients)
        email = EmailMessage(subject, html_content, from_email, recipients)
        email.content_subtype = "html"
        email.send(fail_silently=False)
        print(f"blog created for {instance.id}")
    else:
        print(f"blog already exists for {instance.id}")