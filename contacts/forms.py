from django import forms
from .models import Contact

COUNTRY_CODES = [
    ("+48", "🇵🇱 +48"),
]

class ContactForm(forms.ModelForm):
    country_code = forms.CharField(
        required=False,
        initial="+48",
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone_number", "email", "city", "status"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "required": True, "placeholder": "123456789"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "required": True}),
            "city": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "status": forms.Select(attrs={"class": "form-select", "required": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import ContactStatus
        default_statuses = ["new", "in progress", "lost", "outdated"]
        for status_name in default_statuses:
            ContactStatus.objects.get_or_create(name=status_name)
        
        if self.instance and self.instance.pk:
            phone_value = self.instance.phone_number
            if phone_value and phone_value.startswith("+48"):
                self.initial["country_code"] = "+48"
                self.initial["phone_number"] = phone_value[3:].strip()
        else:
            self.initial["country_code"] = "+48"

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number", "").strip()
        country_code = cleaned_data.get("country_code", "+48")
        
        if phone_number:
            digits_only = "".join(filter(str.isdigit, phone_number))
            if len(digits_only) != 9:
                self.add_error("phone_number", "Phone number must be exactly 9 digits.")
            else:
                cleaned_data["phone_number"] = country_code + phone_number
        
        return cleaned_data

class CsvImportForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": ".csv"}))
