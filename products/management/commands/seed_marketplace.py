from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed marketplace with sellers, shops, categories and products."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Seed command is ready.")
        )
