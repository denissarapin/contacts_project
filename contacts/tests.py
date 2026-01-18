from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from .models import Contact, ContactStatus
from .serializers import ContactSerializer


class ContactModelTest(TestCase):
    def setUp(self):
        self.status = ContactStatus.objects.create(name="new")

    def test_contact_creation(self):
        contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+48123456789",
            email="john.doe@example.com",
            city="Warsaw",
            status=self.status
        )
        
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.phone_number, "+48123456789")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.city, "Warsaw")
        self.assertEqual(contact.status, self.status)
        self.assertIsNotNone(contact.created_at)

    def test_contact_str_representation(self):
        contact = Contact.objects.create(
            first_name="Jane",
            last_name="Smith",
            phone_number="+48987654321",
            email="jane.smith@example.com",
            city="Krakow",
            status=self.status
        )
        
        self.assertEqual(str(contact), "Jane Smith")

    def test_contact_phone_number_unique(self):
        Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+48123456789",
            email="john.doe@example.com",
            city="Warsaw",
            status=self.status
        )
        with self.assertRaises(Exception):
            Contact.objects.create(
                first_name="Jane",
                last_name="Doe",
                phone_number="+48123456789",
                email="jane.doe@example.com",
                city="Warsaw",
                status=self.status
            )


class ContactSerializerTest(APITestCase):
    def setUp(self):
        self.status = ContactStatus.objects.create(name="new")

    def test_serializer_requires_phone_and_email_on_create(self):
        serializer = ContactSerializer(data={
            "first_name": "John",
            "last_name": "Doe",
            "city": "Warsaw",
            "status": "new"
        })
        
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)
        self.assertIn("email", serializer.errors)

    def test_serializer_allows_phone_and_email_optional_on_update(self):
        contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="+48123456789",
            email="john.doe@example.com",
            city="Warsaw",
            status=self.status
        )
        
        serializer = ContactSerializer(
            instance=contact,
            data={
                "first_name": "Jane",
                "last_name": "Smith",
                "city": "Krakow",
                "status": "new"
            },
            partial=True
        )
        
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_serializer_validates_successfully_with_all_fields(self):
        serializer = ContactSerializer(data={
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+48123456789",
            "email": "john.doe@example.com",
            "city": "Warsaw",
            "status": "new"
        })
        
        self.assertTrue(serializer.is_valid(), serializer.errors)
        contact = serializer.save()
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.email, "john.doe@example.com")


class CsvImportTest(TestCase):

    def setUp(self):
        self.default_status = ContactStatus.objects.create(name="new")

    def test_csv_import_creates_contacts(self):
        from django.test import Client
        csv_content = "first_name,last_name,phone_number,email,city,status\n"
        csv_content += "John,Doe,+48123456789,john.doe@example.com,Warsaw,new\n"
        
        csv_file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )
        
        client = Client()
        response = client.post('/import/', {'file': csv_file})
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.status.name, "new")

    def test_csv_import_normalizes_polish_status_to_english(self):
        from django.test import Client
        from .views import STATUS_NAME_MAPPING
        csv_content = "first_name,last_name,phone_number,email,city,status\n"
        csv_content += "Jan,Kowalski,+48111111111,jan.kowalski@example.com,Warsaw,nowy\n"
        
        csv_file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )
        
        client = Client()
        response = client.post('/import/', {'file': csv_file})
        contact = Contact.objects.first()
        self.assertEqual(contact.status.name, "new")
        polish_status = ContactStatus.objects.filter(name="nowy").first()
        self.assertIsNone(polish_status, "Polish status 'nowy' should not be created")

    def test_csv_import_skips_incomplete_rows(self):
        from django.test import Client
        csv_content = "first_name,last_name,phone_number,email,city,status\n"
        csv_content += "John,Doe,+48123456789,john.doe@example.com,Warsaw,new\n"
        csv_content += "Jane,,+48987654321,jane@example.com,Warsaw,new\n"
        
        csv_file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )
        
        client = Client()
        response = client.post('/import/', {'file': csv_file})
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.first_name, "John")
