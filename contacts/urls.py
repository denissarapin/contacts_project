from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.contact_list, name="contact_list"),
    path("create/", views.contact_create, name="contact_create"),
    path("<int:contact_id>/edit/", views.contact_update, name="contact_update"),
    path("<int:contact_id>/delete/", views.contact_delete, name="contact_delete"),
    path("import/", views.import_contacts, name="import_contacts"),
]
