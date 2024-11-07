# E-commerce Django Application

This project is a simple e-commerce application built with Django. It allows users to browse products, filter them by categories and tags, and add them to their cart or delete an order. It includes custom error handling, page caching, and a dynamic navbar that adjusts based on user authentication. The project also includes  user registration, login, logout, and tracking user activity.

## Features
- **User Registration**:  Allows new users to register with the `RegisterUserForm`.
- **User Login**: Allows users to log in with their credentials.
- **User Logout**: Provides a logout functionality that redirects users to the login page.
- **User Activity Tracking**: Updates the user's `last_active_datetime` field upon every request when authenticated.
- **Main Page**: Displays a paginated list of products.
- **Category Page**: Allows filtering products by categories, price, and tags.
- **Search Functionality**: Enables searching for products by name.
- **Sorting**: Products can be sorted by `Price` and `Quantity` field.
- **Cart**: Users can add products to their shopping cart.
- **Contact Page**: Simple contact page.
- **Custom Error Pages**:  404 and 500 error pages are set up for improved user experience.


## URL Patterns

- `/` : Main page showing all products.
- `/category/` : Category page showing all the product.
- `/category/<slug:slug>` : Category page with products filtered by category.
- `/order/cart` : Showing selected items of cart.
- `/register/` : To create a new user account.
- `/login/` :  To log into the app.
- `Logout` : Log out with `/logout/`.


## Models

- **Product**: Represents a product in the store.
- **ProductTag**: Represents tags that can be assigned to products.
- **Category**: Represents a product category.
- **CartItem**: Represents an item in the user's cart. Linked to a `UserCard` model.

### `UserCard`
- One-to-one relationship with the `CustomUser` model.

## Custom Template Tags
Custom template tags are used to modify data in templates. In this project, we have a `cut` filter to replace parts of a string.

## Context Processors
Context processors make specific variables available in all templates without explicitly passing them in views. In this project, we have two context processors:

- Product Count: Returns the count of products in the current user's cart.
- Parent Categories: Retrieves all top-level categories.

## Custom Model Manager
We have a custom `ProductManager` that overrides Django's default `Manager` to include a method for prefetching related fields (category and tags) in product queries to optimize database queries.

## Views

### Main Page:
Displays the main page with a paginated list of products. Products are fetched using a custom `join_related_tables` method in the `ProductManager`.

### Category Page:
Handles the category view, including filtering by categories, price range, tags, search functionality, and sorting.

### RegisterPage
A `CreateView` that allows new users to register. Automatically logs in the user after a successful registration.

### Contact Page:
A simple contact page view.


## base.html Template

### The navbar in `base.html` is cached for 60 seconds per user and includes:

- Links to main sections such as "Home," "Shop," "Contact," and category dropdowns.
- Cart icon displaying the number of items.
- User icon with login/logout functionality based on authentication status.

## Middleware

### UserActiveMiddleware:
 
- Tracks authenticated users' last active time by updating the `last_active_datetime` field
- Sets session expiry to 60 seconds after user activity.