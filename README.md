Syrian System for Marketing & Handicrafts

A full-stack web platform designed to support the marketing and sale of Syrian handicrafts and handmade products.

The system connects buyers, sellers, and bazaar organizers through a centralized marketplace with product management, online ordering, messaging, notifications, reports, and AI-powered gift recommendations.

Live Demo

"View Live Website" (https://marketingsystem.onrender.com)

«The application is hosted on Render's free tier, so the first load may take a short time if the server has been inactive.»

Main Features

User Accounts & Roles

- Buyer, Seller, and Bazaar Organizer accounts
- User registration and authentication
- Role-based dashboards and permissions
- User profile management

Shops & Products

- Sellers can create and manage their shops
- Product and category management
- Product images and detailed product pages
- Search and filtering
- Price sorting
- Flash offers and advertisements

Shopping System

- Shopping basket
- Product quantity management
- Wishlist
- Order placement
- Multiple delivery options
- Order status tracking

Reviews & Interaction

- Buyers can comment on products after purchasing
- Sellers can reply to customer comments

Messaging

- Direct chat between buyers and sellers
- Conversation inbox
- Unread message tracking

Notifications

Notifications are provided for important system events such as:

- New orders
- Order approval or rejection
- Order tracking updates
- New comments and replies
- Bazaar booking requests and updates

Bazaar Management

Bazaar organizers can:

- Create and manage bazaars
- Define location, dates, and table cost
- Review seller booking requests
- Approve or reject bookings

Sellers can:

- Browse available bazaars
- Request a table reservation
- View and cancel their bookings

Reports

Sellers can view reports related to:

- Products
- Orders
- Business activity

AI Gift Recommendation

The system includes an AI-powered gift recommendation feature.

Users can enter information such as:

- Budget
- Occasion
- Age
- Gender
- Relationship

The system then recommends suitable products available in the marketplace.

Technologies Used

Backend

- Python
- Django

Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript

Database

- PostgreSQL in production
- SQLite for development/testing

Deployment & Storage

- Render
- Gunicorn
- WhiteNoise
- Cloudinary

Additional Technologies

- Git & GitHub
- REST/API integration
- AI-based recommendation integration

Project Structure

The project is organized into multiple Django applications, including:

- "users"
- "shops"
- "products"
- "categories"
- "baskets"
- "orders"
- "wishlist"
- "comments"
- "advertisement"
- "offers"
- "chat"
- "notifications"
- "bazaar"
- "reports"
- "recommendations"

Local Installation

Clone the repository:

git clone https://github.com/Nour-Nasan/marketingsystem.git
cd marketingsystem

Create and activate a virtual environment:

python -m venv venv

Install the required packages:

pip install -r requirements.txt

Apply database migrations:

python manage.py migrate

Run the development server:

python manage.py runserver

Environment Variables

Some configuration values should be stored as environment variables rather than directly in the source code, such as:

SECRET_KEY=your-secret-key
DEBUG=True

Production deployment may also require database and Cloudinary configuration variables.

Project Purpose

This project was developed as a graduation project in Software Engineering.

Its goal is to provide a digital marketplace that supports Syrian handicrafts, helps small sellers showcase their products, facilitates communication with customers, and provides tools for online sales and participation in bazaars.

Author

Nour Nasan

Software Engineer | Full-Stack Developer

GitHub: "Nour-Nasan" (https://github.com/Nour-Nasan)
