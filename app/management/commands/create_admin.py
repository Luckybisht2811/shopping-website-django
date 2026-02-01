from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create or reset admin user safely"

    def handle(self, *args, **kwargs):
        username = "admin"
        email = "admin@gmail.com"
        password = "admin@123"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            }
        )

        # ALWAYS reset password
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.email = email
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Admin user created"))
        else:
            self.stdout.write(self.style.SUCCESS("Admin password reset"))
