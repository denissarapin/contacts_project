import csv
import io
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import ContactForm, CsvImportForm
from .models import Contact, ContactStatus
from .services import get_current_weather_for_city

STATUS_NAME_MAPPING = {
    "nowy": "new",
    "zagubiony": "lost",
    "w trakcie": "in progress",
    "nieaktualny": "outdated",
}


def contact_list(request):
    search_query = (request.GET.get("q") or "").strip()
    sort_key = (request.GET.get("sort") or "last_name").strip()

    contacts_qs = Contact.objects.select_related("status").all()

    if search_query:
        contacts_qs = contacts_qs.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(phone_number__icontains=search_query)
            | Q(city__icontains=search_query)
        )

    if sort_key == "created_at":
        contacts_qs = contacts_qs.order_by("-created_at")
    else:
        contacts_qs = contacts_qs.order_by("last_name", "first_name")

    city_names = list({c.city.strip() for c in contacts_qs if c.city and c.city.strip()})
    weather_by_city = {}
    for city in city_names:
        weather_by_city[city] = get_current_weather_for_city(city)

    context = {
        "contacts": contacts_qs,
        "search_query": search_query,
        "sort_key": sort_key,
        "weather_by_city": weather_by_city,
    }
    return render(request, "contacts/contact_list.html", context)


@require_http_methods(["GET", "POST"])
def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact created.")
            return redirect("contacts:contact_list")
    else:
        form = ContactForm()
    return render(request, "contacts/contact_form.html", {"form": form, "title": "Add contact"})


@require_http_methods(["GET", "POST"])
def contact_update(request, contact_id: int):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated.")
            return redirect("contacts:contact_list")
    else:
        form = ContactForm(instance=contact)
    return render(request, "contacts/contact_form.html", {"form": form, "title": "Edit contact"})


@require_http_methods(["POST"])
def contact_delete(request, contact_id: int):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, "Contact deleted.")
    return redirect("contacts:contact_list")


@require_http_methods(["GET", "POST"])
def import_contacts(request):
    if request.method == "POST":
        form = CsvImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data["file"]
            try:
                decoded_text = uploaded_file.read().decode("utf-8")
            except UnicodeDecodeError:
                decoded_text = uploaded_file.read().decode("utf-8-sig")

            reader = csv.DictReader(io.StringIO(decoded_text))
            created_count = 0
            skipped_count = 0

            default_status = ContactStatus.objects.first()
            if not default_status:
                default_status = ContactStatus.objects.create(name="new")

            for row in reader:
                first_name = (row.get("first_name") or "").strip()
                last_name = (row.get("last_name") or "").strip()
                phone_number = (row.get("phone_number") or "").strip()
                email = (row.get("email") or "").strip()
                city = (row.get("city") or "").strip()
                status_name = (row.get("status") or "").strip()

                if not (first_name and last_name and phone_number and email and city):
                    skipped_count += 1
                    continue

                status = default_status
                if status_name:
                    normalized_status_name = STATUS_NAME_MAPPING.get(status_name.lower(), status_name)
                    status, _ = ContactStatus.objects.get_or_create(name=normalized_status_name)

                try:
                    Contact.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        email=email,
                        city=city,
                        status=status,
                    )
                    created_count += 1
                except IntegrityError:
                    skipped_count += 1

            messages.success(request, f"Import finished. Created: {created_count}, Skipped: {skipped_count}.")
            return redirect("contacts:contact_list")
    else:
        form = CsvImportForm()

    return render(request, "contacts/import_contacts.html", {"form": form})

