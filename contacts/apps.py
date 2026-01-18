from django.apps import AppConfig


class ContactsConfig(AppConfig):
    name = 'contacts'

    def ready(self):
        from .models import ContactStatus
        default_statuses = ["new", "in progress", "lost", "outdated"]
        for status_name in default_statuses:
            ContactStatus.objects.get_or_create(name=status_name)
