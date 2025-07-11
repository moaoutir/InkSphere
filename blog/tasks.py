from celery import shared_task


@shared_task(bind=True)
def process_newsletter_task(self):
    pass
