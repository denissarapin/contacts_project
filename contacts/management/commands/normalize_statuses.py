from django.core.management.base import BaseCommand
from contacts.models import Contact, ContactStatus

STATUS_NAME_MAPPING = {
    "nowy": "new",
    "zagubiony": "lost",
    "w trakcie": "in progress",
    "nieaktualny": "outdated",
}


class Command(BaseCommand):
    help = "Migrates contacts from Polish status names to English status names"

    def handle(self, *args, **options):
        migrated_count = 0

        for polish_name, english_name in STATUS_NAME_MAPPING.items():
            try:
                polish_status = ContactStatus.objects.get(name=polish_name)
                english_status, _ = ContactStatus.objects.get_or_create(name=english_name)

                contacts_count = Contact.objects.filter(status=polish_status).count()
                
                if contacts_count > 0:
                    Contact.objects.filter(status=polish_status).update(status=english_status)
                    migrated_count += contacts_count
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Migrated {contacts_count} contact(s) from '{polish_name}' to '{english_name}'"
                        )
                    )

                if not Contact.objects.filter(status=polish_status).exists():
                    polish_status.delete()
                    self.stdout.write(
                        self.style.SUCCESS(f"Deleted status '{polish_name}' (no longer in use)")
                    )
            except ContactStatus.DoesNotExist:
                pass
        
        if migrated_count == 0:
            self.stdout.write(self.style.WARNING("No Polish statuses found to migrate."))
        else:
            self.stdout.write(
                self.style.SUCCESS(f"\nTotal contacts migrated: {migrated_count}")
            )
