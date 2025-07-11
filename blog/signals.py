from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.core.mail import EmailMessage


from .models import Post
from .tasks import process_newsletter_task

from dotenv import load_dotenv
import os

load_dotenv(".env.local")


@receiver(post_save, sender=Post)
def create_profile(sender, instance, created, **kwargs):
    if created:
        domain = os.environ.get("domain")
        post_url = reverse("post-detail", kwargs={"pk": instance.pk})
        full_url = domain.rstrip("/") + post_url
        topic_blog = (
            instance.title + " " + instance.content + "\n blog url: " + full_url
        )
        subject = f"Ink Sphere: {instance.title} by {instance.author.username}"
        recipients = [profile.email for profile in instance.author.profile.subscribers.all()]
        process_newsletter_task.delay(
            topic_blog=topic_blog,
            full_url=full_url,
            subject=subject,
            recipients=recipients,
        )
    # else:
    #     print(f"blog already exists for {instance.id}")
