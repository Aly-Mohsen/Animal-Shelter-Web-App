# 🐾 Paws & Whiskers — Animal Shelter Web App

A Django-based animal shelter web application that helps users discover animals available for adoption. The project combines animal browsing, search and filtering, user authentication, and an integrated chatbot, with an emphasis on maintainable backend development and automated quality assurance.

Built with **Python, Django, PostgreSQL, Bootstrap 5, and JavaScript**.

## ✨ Features

### 🐶 Animal Management and Discovery
- Browse available animals through the shelter interface.
- View individual animal details.
- Search and filter animal listings.
- Organize animals by type and breed.
- Store animal information, including gender, age, weight, status, and photos.
- Manage animal records through Django's administration interface.

### 🔐 User Authentication
- User registration and login.
- Custom user model with profile information.
- User profile fields for full name, phone number, governorate, and profile photo.
- Post-registration redirect handling and validation.

### 🤖 Chatbot Integration
- Integrated chatbot interface for interacting with the shelter website.
- Backend endpoint for processing chatbot messages.
- Input validation for missing, blank, non-string, and oversized messages.
- Error handling for unsuccessful chatbot requests.
- Frontend fallback behavior when the chatbot API returns an error.
- Safe rendering of chatbot responses, including HTML-like content.
- Automated tests using mocked responses to avoid unnecessary external API calls during testing.

### 🧪 Automated Testing and Quality Assurance
- Automated tests for animal listings, filtering, and detail pages.
- Authentication and registration redirect tests.
- Chatbot API validation and response tests.
- Browser-based tests for chatbot interactions and error handling.
- Regression coverage for unsafe redirects, HTML rendering, HTTP errors, and typing-indicator cleanup.

The latest recorded test run passed **23 tests, with 3 subtests passing**.

### 🗄️ Database and Data Integrity
- PostgreSQL database integration.
- Relational models for animals, animal types, breeds, and adoption applications.
- Foreign-key deletion behavior configured for relevant relationships.
- Django migrations for database schema changes.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 5.2.6 | Web framework |
| PostgreSQL | Relational database |
| HTML5 / CSS3 | Page structure and styling |
| JavaScript | Frontend interactions |
| Bootstrap 5 | Responsive UI components |
| django-crispy-forms | Form rendering |
| crispy-bootstrap5 | Bootstrap 5 form integration |
| django-environ | Environment-based configuration |
| Pillow | Image processing |
| Playwright | Browser-based testing |
| Django testing framework | Application and endpoint tests |

## 📁 Project Structure

```text
Animal-Shelter-Web-App/
├── chatbot/
│   ├── migrations/
│   ├── tests.py
│   └── test_browser.py
├── media/
│   └── animals/
├── shelter/
│   └── migrations/
├── shelter_project/
├── static/
│   ├── chatbot/
│   │   ├── css/
│   │   └── js/
│   └── shelter/
│       ├── css/
│       └── images/
├── templates/
│   ├── chatbot/
│   ├── partials/
│   ├── registration/
│   └── shelter/
├── manage.py
├── requirements.txt
└── README.md
```

*Note: This tree highlights the main application components. Individual files and directories may vary as development continues.*

## ⚙️ Getting Started

### Prerequisites

Install the following before setting up the project:

- Python compatible with the project's dependencies.
- PostgreSQL.
- Git.
- pip and Python virtual environment support.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Animal-Shelter-Web-App
```

Replace `<your-repository-url>` with the actual Git repository URL.

### 2. Create and Activate a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use an appropriate activation method for your environment rather than changing system-wide security settings unnecessarily.

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and configure the settings required by the application.

Example:

```dotenv
SECRET_KEY=replace-with-a-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=animal_shelter
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

OPENAI_API_KEY=your_openai_api_key
```

The variable names must match those read by the project's Django settings. Keep `.env` out of version control, and never commit real credentials or API keys.

### 5. Create the PostgreSQL Database

Create a PostgreSQL database matching your configured database name and ensure the configured database user has the necessary permissions.

For example, using `psql`:

```sql
CREATE DATABASE animal_shelter;
```

Configure the remaining connection details in `.env`.

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

The Django administration interface is available at `/admin/` when the corresponding routes are enabled.

## 🧪 Running Tests

Run the Django test suite with:

```bash
python manage.py test
```

Run the chatbot tests independently:

```bash
python manage.py test chatbot
```

These commands use Django's test runner. Browser tests may require additional Playwright and browser setup, depending on their implementation and the installed dependencies.

### Current Test Coverage

| Area | Coverage |
|---|---|
| Animal listings | Listing responses |
| Animal discovery | Search and filtering |
| Animal details | Detail-page behavior |
| Authentication | Registration redirects |
| Chatbot API | Input validation and responses |
| Chatbot frontend | Widget interactions |
| Error handling | API failure fallback |
| Rendering safety | HTML-like content treated as text |
| Regression testing | Unsafe redirect handling and UI cleanup |

The test suite is being expanded incrementally, prioritizing application behavior, regression prevention, and reliable error handling.

## 🐾 Adoption Workflow Status

The project includes an `AdoptionApplication` model with application statuses such as pending, approved, rejected, and withdrawn.

However, **the complete public adoption workflow is not yet implemented**. The model and administration support should not be confused with a working user-facing application submission and approval process.

Planned work includes:

- Adoption application forms and submission endpoints.
- Authentication and authorization checks.
- Validation and duplicate-application prevention.
- Application status transitions.
- Transaction-safe updates to related animal and application records.
- Automated tests for invalid requests, permissions, and concurrent operations.

## 🔒 Security and Reliability

The project emphasizes:

- Environment-based configuration for sensitive values.
- Server-side validation of chatbot input.
- Safe handling of chatbot output in the frontend.
- Regression tests for redirect and rendering behavior.
- Database relationships and configured deletion policies.
- Automated verification of important application behavior.

Production deployment still requires a dedicated review of security settings, credentials, database configuration, static and media file handling, logging, and external API reliability.

## 🚧 Roadmap

### Phase 1: Core Application and Regression Testing
- Maintain animal browsing, search, and filtering.
- Expand model and database integrity tests.
- Improve validation and error handling.
- Keep existing functionality stable through regression tests.

### Phase 2: Adoption Workflow
- Implement the user-facing application process.
- Add authorization and application status management.
- Test duplicate requests and transaction behavior.

### Phase 3: API and Integration Testing
- Expand endpoint-level coverage.
- Mock external API dependencies.
- Test persistence, validation failures, and database constraints.

### Phase 4: Browser Automation
- Expand Playwright coverage for important user journeys.
- Add registration, browsing, and future adoption scenarios.
- Improve selector reliability and failure diagnostics.

### Phase 5: Continuous Integration
- Introduce GitHub Actions.
- Run automated tests on relevant pushes and pull requests.
- Add appropriate linting and coverage reporting.
- Document reproducible setup and test execution.

### Phase 6: Future Enhancements
- Complete and refine the adoption experience.
- Evaluate payment integration when the adoption workflow and business requirements are established.
- Prepare the application for production deployment.

## 🎯 Project Goals

Paws & Whiskers is both a web application and a practical software engineering portfolio project. Its development focuses on:

- Maintainable Django architecture.
- Relational database design.
- Secure request handling.
- Automated testing and regression prevention.
- Browser-based quality assurance.
- Reliable external API integration.
- Reproducible development and CI workflows.

The long-term goal is to deliver a reliable animal shelter application supported by meaningful automated tests and professional development practices.