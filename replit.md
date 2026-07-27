# Marketing System (Django Marketplace)

A full-featured Django marketplace/e-commerce application with shops, products, orders, chat, recommendations, and more.

## Stack
- **Framework**: Django 6
- **Database**: SQLite (via `db.sqlite3`)
- **Python**: 3.12

## Running the app
```
python manage.py runserver 0.0.0.0:5000
```
The workflow "Start application" handles this automatically.

## Apps
- `users` – custom user model with roles (buyer, seller, bazaar organizer)
- `shops` – seller shops
- `products` – product listings with images
- `categories` – product categories
- `orders` – order management and tracking
- `baskets` – shopping baskets
- `comments` – product reviews/comments
- `wishlist` – buyer wishlists
- `advertisement` – seller ads
- `offers` – flash offers
- `chat` – buyer-seller messaging
- `recommendations` – AI-powered recommendations via Groq API
- `bazaar` – bazaar event bookings
- `notifications` – in-app notifications
- `reports` – shop visit analytics

## Environment variables
- `GROQ_API_KEY` – required for the AI recommendations feature (Groq API)

## Notes
- Originally configured for MySQL; switched to SQLite for Replit
- `ALLOWED_HOSTS = ['*']` and `CSRF_TRUSTED_ORIGINS` set for Replit's proxy
- No `requirements.txt` was in the original repo; packages are tracked via `pyproject.toml`

## User preferences
