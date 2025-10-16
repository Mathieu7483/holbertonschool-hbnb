<p align="center">
<img src="https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/Logo%20de%20hippocampe%20et%20circuits%20%C3%A9lectroniques.png" width="1000">
</p>

# HBnB - BL and API (Part 2)

## 📆 Project Structure

This project follows a modular structure to ensure maintainability and scalability. The current setup implements the foundation for the Business Logic Layer (BLL), the API, and the in-memory persistence layer.

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   └── persistence/
│       ├── __init__.py
│       └── repository.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

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

## 🔮 Next Steps

* Replace in-memory repository with SQLAlchemy in Part 3
* Add authentication and RBAC
  
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
