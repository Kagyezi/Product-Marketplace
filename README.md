# Product Marketplace Backend

This project is a **simplified Django backend system** for managing products with **role-based access control**, exposing both **HTML-based views** and **REST API endpoints**.

The focus of this submission is on:

* Backend correctness
* Clear permission enforcement
* Clean separation of concerns
* Readable and maintainable code

The project intentionally avoids over-engineering and demonstrates a solid **beginner-to-intermediate backend design**.

---

## Features Overview

### User Roles

The system supports **two roles**:

* **Admin**

  * Create products
  * Update products
  * Delete products
  * View all products belonging to their business

* **Viewer**

  * View products only (read-only access)

Roles are enforced at the **backend level**, not just in the UI.

---

### Product Management

* Products are created by Admin users
* Products are **immediately public** once created
* No approval or draft workflow
* Each product belongs to a business owned by an Admin

This design keeps the system simple and predictable while still enforcing proper access control.

---

## Tech Stack

* **Backend Framework:** Django
* **API Layer:** Django REST Framework (DRF)
* **Authentication:**

  * Session-based authentication for HTML views
  * JWT authentication for API endpoints
* **Database:** SQLite (development)
* **Environment Variables:** python-dotenv

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd product-marketplace
```

---

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
```

> ⚠️ The `.env` file is excluded from version control and should not be committed.

---

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. (Optional) Create a Superuser

```bash
python manage.py createsuperuser
```

---

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```
http://127.0.0.1:8000/
```

---

## Authentication & Authorization

* Users sign up and log in using Django’s authentication system
* During signup/login, users select a role:

  * **Admin**
  * **Viewer**
* Role-based access is enforced:

  * Admins can modify data
  * Viewers have read-only access
* API endpoints use **JWT authentication**
* HTML views use **session-based authentication**

This ensures consistent behavior across both UI and API layers.

---

## API Overview

The project exposes REST API endpoints for product management.

### Public Endpoints

* `GET /api/products/public/`
  Returns all products (read-only, no authentication required)

### Admin Endpoints (JWT required)

* `GET /api/products/`
* `POST /api/products/`
* `GET /api/products/<id>/`
* `PUT /api/products/<id>/`
* `DELETE /api/products/<id>/`

Only Admin users can create, update, or delete products.
Viewers receive `403 Forbidden` for restricted actions.

---

## Tech Decisions & Assumptions

### Role Simplification

Only **Admin** and **Viewer** roles were implemented to:

* Reduce complexity
* Keep permissions explicit and easy to reason about
* Avoid redundant approval workflows

---

### No Approval Workflow

Products become visible immediately after creation.

This was a deliberate decision to:

* Eliminate hidden states
* Avoid unnecessary business logic
* Make system behavior transparent

---

### Backend-First Design

* Business rules live in the backend
* UI is intentionally minimal
* API and UI share the same permission logic
* No duplication of rules across layers

---

### Database Choice

* SQLite is used for development simplicity
* The schema is compatible with PostgreSQL/MySQL for production use

---

## Known Limitations

* No pagination or search on product listings
* No automated test suite included
* SQLite is not suitable for production scale
* Basic UI intended only to demonstrate backend behavior

### Planned but Not Implemented

* An **AI-powered chatbot** for querying product information
  This was planned as an enhancement but excluded from the final submission to prioritize core backend correctness and time constraints.

---

## Additional Notes

* The project is structured to be easily extended
* Possible future improvements include:

  * Product search and filtering
  * Pagination
  * AI chatbot integration
  * Improved frontend
  * Automated testing

---

## Summary

This project demonstrates:

* Clean Django project structure
* Correct role-based access control
* Clear separation between UI and API
* Thoughtful scope management

The implementation focuses on **clarity, correctness, and extensibility**, making it a strong foundation for further development.

