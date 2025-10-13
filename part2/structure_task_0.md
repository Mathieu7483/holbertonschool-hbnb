hbnb/
├── app/
│   ├── __init__.py                  # Flask app initialization
│   ├── api/                         # Layer Présentation (endpoints)
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/                      # Layer Logic
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/                    # Layer Facade
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/                # Layer Persistance
│       ├── __init__.py
│       ├── repository.py
├── run.py                           # Entry point of the app
├── config.py                        # Environment config
├── requirements.txt                 # Python dependance
├── README.md                        # Project Documentation
