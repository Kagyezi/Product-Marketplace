# Product-Marketplace
The aim of this project is to build a small system where businesses can manage products for sale.

Product Marketplace Backend with AI Chatbot
Overview

This project implements a backend system for managing business products with role-based permissions, approval workflows, and an AI-powered chatbot.

Businesses can create products, manage users with different roles, and control which products are visible to the public.
Only approved products are exposed externally and to the AI chatbot.

The frontend was intentionally excluded to focus on backend correctness, clarity, and reasoning, as allowed by the assignment.

Features Implemented
✅ Backend (Django + DRF)

JWT-based authentication

Multi-business support

Custom user model with roles:

Admin

Editor

Approver

Viewer

Product lifecycle:

Draft

Pending approval

Approved

Role-based permission enforcement

Public endpoint exposing approved products only

✅ AI Chatbot

Users can ask questions about products

Chatbot only has access to approved products

AI responses generated using OpenAI API

Chat history stored (question, answer, timestamp)

Tech Stack

Backend: Django, Django REST Framework

Authentication: JWT (SimpleJWT)

AI Integration: OpenAI API

Database: SQLite (default, easily replaceable)

Business Rules Enforced
Action	Allowed Roles
Create / edit product	Admin, Editor
Approve product	Admin, Approver
View all products	Internal users
View approved products	Public
Chatbot visibility	Approved products only

All rules are enforced at the API level, not the frontend.

Project Structure
accounts/   → Users, roles, businesses  
products/   → Product models, permissions, endpoints  
chatbot/    → AI chatbot & chat history  


Each app has a clear responsibility to keep the system simple and maintainable.

API Endpoints
Authentication
POST /api/auth/login/

Products (Internal)
GET    /api/products/
POST   /api/products/
PUT    /api/products/{id}/
POST   /api/products/{id}/approve/

Products (Public)
GET /api/products/public/

AI Chatbot
POST /api/chat/

AI Chatbot Design

The chatbot follows a controlled prompt strategy:

Queries approved products from the database

Injects product data into the AI prompt

Prevents hallucinations by restricting context

Stores each interaction for traceability

This approach prioritizes data safety and correctness over complexity.

Setup Instructions
1. Clone repository
git clone https://github.com/your-username/product-marketplace-backend.git
cd product-marketplace-backend

2. Create virtual environment
python -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Environment variables

Create a .env file using .env.example as reference.

5. Migrate & run
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Assumptions & Simplifications

One business per user

Roles are static and enum-based

Approval is a simple status transition

SQLite used for simplicity

No frontend included by design

Tradeoffs & Design Decisions

Used role-based permissions instead of object-level ACLs to keep logic readable

AI chatbot uses prompt-injection rather than full RAG for simplicity

Frontend omitted to focus on backend fundamentals

Possible Improvements

Add automated tests

Pagination & filtering

Role management UI

Advanced AI retrieval (RAG)

Rate limiting & caching

Final Notes

This project prioritizes clarity, correctness, and reasoning over feature completeness.
It demonstrates strong fundamentals in backend design, permissions, and safe AI integration.

👤 Author

Kagyezi Davis
Electrical Engineer | Backend & AI Enthusiast