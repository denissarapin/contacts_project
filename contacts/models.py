from django.db import models

class ContactStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=120)
    status = models.ForeignKey(ContactStatus, on_delete=models.PROTECT, related_name="contacts")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
