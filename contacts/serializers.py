from rest_framework import serializers
from .models import Contact, ContactStatus

class ContactStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactStatus
        fields = ["id", "name"]

class ContactSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field="name", queryset=ContactStatus.objects.all())
    phone_number = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Contact
        fields = ["id", "first_name", "last_name", "city", "status", "created_at", "phone_number", "email"]
        read_only_fields = ["id", "created_at"]
    
    def validate(self, data):
        if self.instance is None:
            errors = {}
            if not data.get('phone_number'):
                errors['phone_number'] = "This field is required when creating a contact."
            if not data.get('email'):
                errors['email'] = "This field is required when creating a contact."
            if errors:
                raise serializers.ValidationError(errors)
        return data