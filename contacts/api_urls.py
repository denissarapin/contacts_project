from django.urls import path
from .api_views import ContactListCreateApiView, ContactDetailApiView

urlpatterns = [
    path("contacts/", ContactListCreateApiView.as_view(), name="api_contacts_list_create"),
    path("contacts/<int:pk>/", ContactDetailApiView.as_view(), name="api_contacts_detail"),
]