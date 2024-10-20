# Destion Innovation E-commerce Project

This project is a simple, RESTful API for managing products and orders in an e-commerce system, built using Django and Django REST Framework (DRF). The API supports product listing, order placement, and order management, with role-based access control for regular users and admins.

## Features

- **Product Management**: Create, update, delete, and retrieve product information. (Admin access only for modification)
- **Order Management**: Place and retrieve orders for authenticated users.
- **Role-Based Access Control**: Admin users can manage orders and products, while regular users can place and view their own orders.
- **Stock Management**: Automatically adjust product stock levels when orders are placed or canceled.
- **Order Status Management**: Admins can update the status of orders (ship, deliver, or cancel).

## API Endpoints

### Product Endpoints

- `GET /products/`: Retrieve a list of all products.
- `GET /products/<id>/`: Retrieve details for a specific product.
- `POST /products/`: Create a new product (Admin only).
- `PUT /products/<id>/`: Update product information (Admin only).
- `DELETE /products/<id>/`: Delete a product (Admin only).

### Order Endpoints

- `POST /orders/`: Create a new order (Authenticated users only).
- `GET /orders/`: List all orders for the authenticated user.
- `GET /orders/<id>/`: Retrieve details for a specific order (Authenticated users for their orders, Admin for all orders).
- `PUT /orders/<id>/cancel`: Cancel a pending order (Authenticated users for their own orders).
  
### Admin Order Management Endpoints

- `PUT /orders/<id>/ship`: Mark an order as shipped (Admin only).
- `PUT /orders/<id>/deliver`: Mark an order as delivered (Admin only).

## Installation

### Prerequisites

- Python 3.x
- Django 4.x
- Django REST Framework
- A database setup (SQLite or PostgreSQL)

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ecommerce-rest-api.git
   cd ecommerce-rest-api
   ```

2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a Superuser (Admin account):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the API in your Browser or Postman:**
   - API root: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

## Usage

### Admin Actions

- Admins can create, update, and delete products via `/products/` endpoints.
- Admins can update order statuses (ship, deliver) via `/orders/` endpoints.

### Customer Actions

- Users can register, log in, and place orders via the `/orders/` endpoint.
- Users can view their orders and cancel pending orders.

### Product Stock

- Product stock is automatically reduced when an order is placed.
- Canceling an order will restock the associated products.

## Models

### Product

- `name`: The name of the product.
- `description`: The product's description.
- `price`: The price of the product.
- `stock`: The current stock level of the product.
- `created_at`: The timestamp of when the product was added.
- `updated_at`: The timestamp of the latest update to the product.

### Order

- `customer`: A reference to the user placing the order.
- `products`: A many-to-many relationship with `Product`, managed through `OrderItem`.
- `total_price`: The total cost of the order.
- `ordered_at`: The timestamp of when the order was placed.
- `status`: The current status of the order (pending, shipped, delivered, canceled).

### OrderItem

- `order`: A foreign key linking to the `Order` model.
- `product`: A foreign key linking to the `Product` model.
- `quantity`: The number of units of the product ordered.
- `price`: The price of the product at the time of ordering.

## Permissions

- **Admins**: Can manage products and orders.
- **Authenticated Users**: Can place orders and view their own orders.
- **Unauthenticated Users**: Have read-only access to products but cannot place orders.

## Contact

For any inquiries or support, feel free to reach out:

- **Email**: praweengupta@example.com
