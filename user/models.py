from PIL import Image

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pictures")
    subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image.width > 300 or self.image.height > 300:
            img = Image.open(self.image.path)
            img.thumbnail((300, 300))
            img.save(self.image.path)
        print(f"Profile for {self.user.username} saved with image {self.image.name}")

class AuthorSubscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_subscription')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')