# Student Management API

Author: Matthew Kirik, IP-03 group

## Project Description

This project is a RESTful API for a Student Management System, designed for use by school head teachers, teachers, and students. It allows for administrative tasks such as creating new courses, classes, user accounts (for students, teachers, and heads), and assigning students to classes and classes to courses. Teachers can use the API to access and submit student marks, and students can view their marks.

## Architecture

The application follows the layered architecture pattern for maintainability and separation of concerns:

1. **Data Access Layer:** Comprised of Django models to abstract the database and perform CRUD operations.
2. **Business Logic Layer:** Implemented as Python services to encapsulate the business logic, avoiding placing this logic in views and ensuring that the views remain light and concerned only with handling HTTP requests and responses.
3. **Presentation Layer:** Django views, which receive HTTP requests, call the appropriate services, and return HTTP responses.

The application is divided into four main Django apps or modules - `users`, `courses`, `classes`, and `marks`. Each of these is responsible for a different domain of the application and contains its own models, views, services, and URL configurations.

## Tech Stack

- **Python**: The primary language for backend logic, selected for its simplicity and the vast ecosystem of libraries available for web development.
- **Django**: A high-level Python web framework that follows the model-template-views architectural pattern. It's robust, versatile and comes with many built-in features such as an ORM, authentication, and an admin interface, reducing the amount of boilerplate code needed.
- **Django REST Framework**: A powerful and flexible toolkit for building Web APIs on top of Django. It offers features such as authentication and permission policies, serializers, viewsets, and routers.
- **Django REST framework JWT**: A JSON Web Token authentication plugin for Django REST Framework.

## How to Run

First, install all required Python libraries by running `pip install -r requirements.txt`. Then, run `python manage.py migrate` to apply migrations. Finally, you can start the server by running `python manage.py runserver`. This will start the server at `localhost:8000`.
