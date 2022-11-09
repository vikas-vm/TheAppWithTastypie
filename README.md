<p align="center">
    <h1>TheApp(Week-1)</h1>
</p>

## Installation

- `git clone https://github.com/vikas-vm/TheApp-Week-1-.git`
- `git checkout vi-dev`
- `python/python3 -m venv env`
- `source activate env`
- `pip install -r requirements.txt`
- `python manage.py runserver`

## Built With

- Python
- Django
- DjangoRestFramework
- JWTAuthentication
- DjangoRestFrameworkSimpleJWT
- Django_Filter

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/token/` - Get a token-pair
- `POST /api/auth/token/refresh/` - Refresh an access token

### Merchants

- `GET /api/merchants/` - List all merchants
- `GET /api/merchants/?search=<search>` - Search merchants (merchant name)
- `POST /api/merchants/` - Create a new merchant
- `GET /api/merchants/{id}/` - Retrieve a merchant
- `PUT /api/merchants/{id}/` - Update a merchant
- `DELETE /api/merchants/{id}/` - Delete a merchant

### Stores

- `GET /api/stores/` - List all stores
- `GET /api/stores/?search=<search>` - Search stores (store name and merchant name)
- `GET /api/stores/?merchant=<merchant_id>` - Filter stores by merchant
- `POST /api/stores/` - Create a new store
- `GET /api/stores/{id}/` - Retrieve a store
- `PUT /api/stores/{id}/` - Update a store
- `DELETE /api/stores/{id}/` - Delete a store

### Categories

- `GET /api/categories/` - List all categories
- `GET /api/categories/?search=<search>` - Search categories (category name)
- `GET /api/categories/?parent=<parent_id>` - Filter categories by parent
- `GET /api/categories/?parent__isnull=true` - Filter categories with no parent
- `POST /api/categories/` - Create a new category
- `GET /api/categories/{id}/` - Retrieve a category
- `PUT /api/categories/{id}/` - Update a category
- `DELETE /api/categories/{id}/` - Delete a category

### Items

- `GET /api/items/` - List all items
- `GET /api/items/?search=<search>` - Search items (item name, store name, merchant name, and category name)
- `GET /api/items/?store=<store_id>` - Filter items by store
- `GET /api/items/?category=<category_id>` - Filter items by category
- `POST /api/items/` - Create a new item
- `GET /api/items/{id}/` - Retrieve an item
- `PUT /api/items/{id}/` - Update an item
- `DELETE /api/items/{id}/` - Delete an item

- Postman Collection(API docs with example) - [https://www.postman.com/warped-zodiac-938921/workspace/urbanpiper-onboarding/collection/18650663-ad9b26f1-1c19-4bfd-8981-87518e2a0736?action=share&creator=18650663](https://www.postman.com/warped-zodiac-938921/workspace/urbanpiper-onboarding/collection/18650663-ad9b26f1-1c19-4bfd-8981-87518e2a0736?action=share&creator=18650663)
