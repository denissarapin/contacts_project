from django.contrib import admin
from .models import Contact, ContactStatus

@admin.register(ContactStatus)
class ContactStatusAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "phone_number", "email", "city", "status", "created_at"]
    search_fields = ["first_name", "last_name", "email", "phone_number", "city"]
    list_filter = ["status", "city"]
