from rest_framework import generics
from .models import Contact
from .serializers import ContactSerializer

class ContactListCreateApiView(generics.ListCreateAPIView):
    queryset = Contact.objects.select_related("status").all().order_by("id")
    serializer_class = ContactSerializer

class ContactDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.select_related("status").all()
    serializer_class = ContactSerializer
