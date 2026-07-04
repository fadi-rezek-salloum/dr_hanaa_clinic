# 1. Project Overview & Mission Statement
Dr. Hanaa Clinic is a Django-based web application providing an online presence for Dipl Med. Hanaa Ahmad's medical practice. The primary mission is to offer patients clear information on staff, consultation times (Sprechzeiten), practice closures (Praxisschließzeiten), and a simple contact form.

# 2. High-Level Architecture
The project follows a standard Django monolithic architecture:
- **`core`**: Contains project-wide settings, WSGI/ASGI configurations, and base URL routing.
- **`base`**: The primary app handling main static-like pages (index, impressum, datenschutz) and the contact form logic.
- **`staff`**: Manages staff profiles and specialties.
- **`timing`**: Manages schedules including consultation times, free admissions, and practice closures.
The system uses Django templates for the frontend, SQLite3 as the default database, and WhiteNoise for serving static files in production.

# 3. Database Schema & Data Models
- **`base.models.Contact`**: Records patient inquiries (Vorname, Name, Telefon, E-Mail, Betreff, Nachricht, submitted_at).
- **`staff.models.Staff`**: Represents clinic staff members with fields for picture, title, name, specialty, tags (using `django-taggit`), created, and updated timestamps.
- **`timing.models.FreeAdmission`**: Tracks free admission slots (Wochentag, Startzeit, Endzeit).
- **`timing.models.ConsultationTime`**: Tracks standard consultation times (Wochentag, Startzeit, Endzeit, and a boolean for "Nach Vereinbarung").
- **`timing.models.PracticeClosure`**: Tracks dates when the practice is closed (Startdatum, Enddatum).

# 4. URL Routing & Entry Points
- `/admin/`: Django Administration interface (styled with Jazzmin).
- `/`: Main index page (via `base:index`).
- `/impressum/`: Legal notice page (via `base:impressum`).
- `/datenschutz/`: Privacy policy page (via `base:datenschutz`).
- `/neupatienten/`: Rules, warnings, and registration form download page (via `base:neupatienten`).
- `/contact/`: POST endpoint for the contact form (via `base:contact`).
Media URLs are routed under `/media/` when in DEBUG mode.

# 5. Django Views & Business Logic
The `base` app utilizes Django Class-Based Views (CBVs):
- **`IndexView` (`TemplateView`)**: Renders `base/index.html`. It overrides `get_context_data` to inject all `Staff`, `FreeAdmission`, `ConsultationTime`, and `PracticeClosure` objects into the template context for dynamic rendering.
- **`ImpressumView`, `DatenschutzView`, `NeupatientenView` (`TemplateView`)**: Render static legal and patient informational pages.
- **`ContactView` (`FormView`)**: Handles the submission of the `ContactForm`. On valid submission, it saves the `Contact` to the DB, renders an HTML email using `_email.html`, sends it via SMTP, displays a success message, and redirects to `#contact` on the index page.

# 6. Forms & Validation Rules
- **`ContactForm` (`ModelForm`)**: Linked to the `Contact` model. It defines required HTML5 widgets with placeholders for `vorname`, `name`, `email`, `betreff`, and `nachricht`. `telefon` is optional. The form enforces built-in Django email and length validation.

# 7. Template System & Layout Structure
- **Base Layout**: `_base.html` provides the overarching HTML skeleton.
- **Includes**: `_header.html` (navigation), `_footer.html` (footer info), `_preloader.html` (loading animation), `_email.html` (HTML email structure).
- **Page Templates**: `index.html`, `impressum.html`, `datenschutz.html`, and `neupatienten.html` reside in `templates/base/` and extend the base layout or are included where necessary. Context processors are used to inject authentication and message variables globally.

# 8. Static & Media Asset Management
- **Static Files**: Configured to use `static/` URL and `staticfiles/` root. Managed via `WhiteNoiseMiddleware` (without strict manifest generation) for efficient serving in production.
- **Media Files**: User-uploaded files (like staff pictures) are stored in the `media/` directory and served at `/media/`.

# 9. Environment Variables & Configuration
The project uses `python-dotenv` to load `.env`. Key variables include:
- `SECRET_KEY`: Django cryptographic key.
- Database vars: `DB_HOST`, `DB_NAME`, `DB_PASSWORD`, `DB_PORT`, `DB_USER`.
- Email vars: `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`.

# 10. Email & Notification Systems
- Uses Django's SMTP `EmailBackend` configured to `smtp.gmail.com` on port 587 with TLS.
- Sends an HTML-formatted confirmation email to the user submitting the contact form, utilizing the sender address `praxis@example.com` (while authenticating with `EMAIL_HOST_USER`).

# 11. Administrative Portal (Jazzmin) & Customizations
- The standard Django admin is themed using `django-jazzmin`.
- `JAZZMIN_SETTINGS` configures the site title ("Dipl Med. Hanaa Ahmad"), header, welcome sign, and sets the site logo to `images/favicon.ico`.

# 12. Development & Deployment Workflow
- **Development**: Runs locally on `localhost`. Uses `db.sqlite3` by default.
- **Deployment**: Configured with `ALLOWED_HOSTS` including `ha-praxis.com` and `www.ha-praxis.com`. `CSRF_TRUSTED_ORIGINS` are set for HTTPS. The app expects an HTTPS proxy (`SECURE_PROXY_SSL_HEADER`).
- **Dependencies**: Listed in `requirements.txt`.

# 13. Coding Conventions & Best Practices
- Models feature verbose names (in German) and `__str__` representations for better admin UX.
- URLs are namespaced (`app_name = "base"`).
- Class-Based Views are preferred over Function-Based Views.
- The project follows a modular app structure separating core settings, staff management, timing/schedules, and base views.

# 14. Security & Performance Configurations
- Standard Django middleware handles Security, Sessions, CSRF, and X-Frame-Options.
- Password validators enforce minimum length, similarity checks, and complexity.
- `WhiteNoiseMiddleware` is positioned right after `SecurityMiddleware` for optimal static file performance.

# 15. Developer Cheat Sheet & Quick Commands
- **Run Server**: `python manage.py runserver`
- **Make Migrations**: `python manage.py makemigrations`
- **Apply Migrations**: `python manage.py migrate`
- **Create Superuser**: `python manage.py createsuperuser`
- **Collect Static**: `python manage.py collectstatic`
