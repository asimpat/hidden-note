import random
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from django.contrib.auth import get_user_model
from hidden.models import Message

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with test users and messages"

    def handle(self, *args, **kwargs):
        # Create a superuser if not exists
        admin = User.objects.filter(username="admin").first()
        if not admin:
            admin = User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin123"
            )
            self.stdout.write(self.style.SUCCESS("Superuser created."))

        # Create test users
        usernames = ["alice", "bob", "charlie", "david", "eve"]
        for uname in usernames:
            user = User.objects.filter(username=uname).first()
            if not user:
                user = User.objects.create_user(
                    username=uname,
                    email=f"{uname}@example.com",
                    password="test1234"   # 👈 this will be hashed automatically
                )
                self.stdout.write(self.style.SUCCESS(f"User created: {uname}"))

            # Add random messages for this user
            for _ in range(random.randint(2, 5)):
                Message.objects.create(
                    user=user,
                    message=lorem_ipsum.paragraph()
                )
            self.stdout.write(self.style.SUCCESS(
                f"Messages added for {uname}"))
