# Contacts Management Project

Django web application for managing contacts with REST API support, CSV import functionality, and weather integration.

## Features

- **Contact Management**: Create, read, update, and delete contacts
- **CSV Import**: Bulk import contacts from CSV files with automatic status normalization (Polish → English)
- **REST API**: Full CRUD API endpoints for contacts
- **Weather Integration**: Displays current weather information for each contact's city
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **Status Management**: Customizable contact statuses with normalization

## Tech Stack

- Django 6.0.1
- Django REST Framework
- SQLite (development)
- Bootstrap 5
- Docker & Docker Compose

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/denissarapin/contacts_project.git
cd contacts_project
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Docker Compose (Recommended)

Project is ready for Docker deployment:

```bash
docker-compose up --build
```

This will:
- Build the Docker image
- Run database migrations
- Start the development server on port 8000

Access at `http://localhost:8000/`

## API Endpoints

- `GET /api/contacts/` - List all contacts
- `POST /api/contacts/` - Create new contact
- `GET /api/contacts/{id}/` - Get contact details
- `PUT /api/contacts/{id}/` - Update contact
- `DELETE /api/contacts/{id}/` - Delete contact

**Note:** API returns contacts without `phone_number` and `email` fields in GET responses (for privacy), but these fields are required/optional in POST/PUT requests.

## CSV Import

CSV format should include headers: `first_name,last_name,phone_number,email,city,status`

Status names are automatically normalized:
- `nowy` → `new`
- `zagubiony` → `lost`
- `w trakcie` → `in progress`
- `nieaktualny` → `outdated`

## Testing

Unit tests are implemented for:
- Contact model validation
- API serializer validation
- CSV import with status normalization

Run tests:
```bash
python manage.py test
```

Or with Docker:
```bash
docker-compose exec web python manage.py test
```

## Project Structure

```
contacts_project/
├── config/          # Django project settings
├── contacts/        # Main app
│   ├── api_views.py # REST API views
│   ├── models.py    # Contact and ContactStatus models
│   ├── views.py     # Web views
│   ├── serializers.py # API serializers
│   └── tests.py     # Unit tests
├── templates/       # HTML templates
├── static/          # Static files (JS, CSS)
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment Variables

Optional `.env` file:
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## License

MIT
