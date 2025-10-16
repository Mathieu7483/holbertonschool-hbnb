<p align="center">
<img src="https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/Logo%20de%20hippocampe%20et%20circuits%20%C3%A9lectroniques.png" width="1000">
</p>

# HBnB - BL and API (Part 2)

# 📝 Description
This project represents the second implementation phase of the HBnB application, focused on building the Business Logic and Presentation (RESTful API) layers. It involves transforming the previous UML design into functional code by defining the main entities (User, Place, Review, Amenity) and exposing their functionalities through RESTful endpoints.
Particular attention is paid to Separation of Concerns by using the Facade Pattern to link the API to the business core, and the In-Memory Repository Pattern for temporary data management.

# 📚 Key Concepts

Modular Architecture: Structuring a Python/Flask application into layers (presentation, business_logic, persistence).
RESTful API with Flask: Using the Flask framework and the flask-restx extension for routing, data schema definition, and Swagger documentation.
Facade Pattern: Implementation of the Facade design pattern to simplify complex interactions between the Presentation layer and Business Logic.
Business Logic Classes: Implementation of entity models (partial CRUD) with relationship management and attribute validation.
Serialization: Composing API responses to include extended attributes and related object data (e.g., the owner's username for a Place).

# Exercice Conten
t
0. Project Setup and Package Initialization:

Setting up the modular directory structure.
Configuring the Flask application and flask-restx.
Implementing the Facade Pattern and an In-Memory Repository for temporary object storage.
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

1. Core Business Logic Classes:

Implementation of base classes and concrete classes: User, Place, Review, and Amenity.
Defining attributes and relationships between entities.


2. User Endpoints:

Implementation of partial CRUD endpoints (POST, GET /users, GET /users/<id>, PUT) for user management (without DELETE and without password in responses).


3. Amenity Endpoints:

Implementation of partial CRUD endpoints (POST, GET /amenities, GET /amenities/<id>, PUT) for amenity management.


4. Place Endpoints:

Implementation of partial CRUD endpoints (POST, GET /places, GET /places/<id>, PUT) for place management.
Handling the inclusion of Owner and Amenities data in responses.


5. Review Endpoints:

Implementation of complete CRUD endpoints (POST, GET, PUT, DELETE) for review management (first implementation of deletion).
Handling retrieval of reviews related to a specific place.


6. Testing and Validation:

Implementation of basic validation for all entity models.
Manual black-box testing phase using cURL to verify proper functionality, HTTP status codes, and input/output formats for each endpoint.

## 🧠 Key Concepts Implemented

* ✅ Modular application structure
* ✅ Flask app factory pattern (`create_app`)
* ✅ flask-restx setup with Swagger
* ✅ In-memory repository following the Repository Pattern
* ✅ Facade layer to decouple API and logic
* ✅ Project ready for future integration with SQLAlchemy

## ⚙️ Getting Started

### 🔹 Install dependencies

We recommend using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-restx
```

### 🔹 Run the application

```bash
python3 run.py
```

# 🛠️ Technologies and Tools

* Language: Python 3.8.5
* Web Framework: Flask
* API: flask-restx (for structuring and Swagger documentation)
* Testing Tools: cURL, Postman
* Design: Facade Pattern, Repository Pattern


# ✍️ Authors

<div align="center">

| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Florian Hadjar** | Co-Developer | [@Boubouche1709](https://github.com/Boubouche1709) | 10482@holbertonstudents.com |
| **Mathieu Godalier** | Co-developer | [@Mathieu7483](https://github.com/Mathieu7483) | 11436@holbertonstudents.com |
</div>

# ⚖️ License
This project is licensed under the MIT License. For more details, see the LICENSE file.