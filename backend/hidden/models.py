from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import uuid
import secrets


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "user"
        ADMIN = "admin"

    role = models.CharField(
        max_length=10, choices=RoleChoices.choices, default=RoleChoices.USER)
    secret_link = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.secret_link:
            # Create slug with username + part of uuid
            unique_id = secrets.token_hex(4)  
            self.secret_link = slugify(f"{self.username}-{unique_id}")
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.user.username} at {self.created_at}"

