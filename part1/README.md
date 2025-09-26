<p align="center">
<img src="https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/Logo%20de%20hippocampe%20et%20circuits%20%C3%A9lectroniques.png" width="1000">
</p>



# 📝 Description Part 1
This project, HBnB Evolution, is the initial phase of developing a simplified AirBnB-like application. This part focuses on creating a comprehensive technical documentation blueprint using UML (Unified Modeling Language). The goal is to design the system's architecture and interactions before implementation, ensuring a clear and shared understanding among the team. The application is structured into three main layers: the Presentation Layer, the Business Logic Layer, and the Persistence Layer.

# 📂 Exercise Content
This directory contains the UML diagrams and explanatory notes that form the technical documentation for the project.

[0. High-Level Package Diagram:]() A high-level package diagram illustrating the application's three-layer architecture and the communication between them via the Facade Pattern. This diagram provides an overview of the code's organization.
```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +ServicesAPI
    +UserController
    +PlaceController
    +ReviewController
    +AmenityController
}
class BusinessLogicLayer {
    + User
    + Place
    + Review
    + Amenity
    + HBnBFacade
}
class PersistenceLayer {
    + UserRepository
    + PlaceRepository
    + ReviewRepository
    + AmenityRepository
    + DatabaseConnector
}
PresentationLayer --> BusinessLogicLayer : via HBNB Facade
BusinessLogicLayer --> PersistenceLayer : UsesRepositories
```



[1. Detailed Class Diagram for Business Logic Layer:]() A detailed class diagram for the Business Logic layer. It models the core entities of the application (User, Place, Review, Amenity) with their attributes, methods, and relationships. This diagram is crucial for designing the data models.
```mermaid
classDiagram
    direction TD

    User <|-- Client
    User <|-- Administrator
    User <|-- Owner

    class User{
        - id: String
        - firstName: String
        - lastName: String
        - mail: String
        - password: String
        + register()
        + update()
        + delete()
    }
    
    note for Administrator "Administrators : Florian and Mathieu"

    class Client{
        + book(place)
        + review(place, rating)
    }

    class Administrator{
        + modify(entity)
    }

    class Owner{
        + createPlace(place)
        + updatePlace(place)
        + deletePlace(place)
        + listPlaces()
    }

    Client "1" -- "0..*" ReviewEntity : emits
    Client "1" -- "0..*" PlaceEntity : rent
    Owner "1" -- "0..*" PlaceEntity : possess
    PlaceEntity "1" -- "0..*" ReviewEntity : a

    PlaceEntity "1" *-- "0..*" AmenityEntity : a

    class PlaceEntity{
        - title: String
        - description: String
        - price: Float
        - longitude: Float
        - latitude: Float
    }

    class AmenityEntity{
        - name: String
        - description: String
    }
    
    class ReviewEntity{
        - rating: Int
        - comment: String
    }
```

[2. Sequence Diagrams for API Calls:]() A series of sequence diagrams that illustrate the flow of information and interactions between the different layers for specific use cases, such as user registration, place creation, review submission, and fetching a list of places.
```mermaid
sequenceDiagram
    participant Client(Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database(Backend)

    Client(Frontend)->>API: POST /users/register
    activate API
    Note right of API: User registration request

    API->>BL: registerUser(userData)
    activate BL

    BL->>Database(Backend): saveUser(userData)
    activate Database(Backend)

    Database(Backend)-->>BL: new user record
    deactivate Database(Backend)

    BL-->>API: success response
    deactivate BL

    API-->>Client(Frontend): HTTP Created
    deactivate API
```

```mermaid
sequenceDiagram
    participant Owner(Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database(Backend)

    Owner(Frontend)->>API: POST /Owner/place/register
    activate API
    Note right of API: Owner place registration request

    API->>BL: registerPlace(OwnerData)
    activate BL

    BL->>Database(Backend): savePlace(OwnerData)
    activate Database(Backend)

    Database(Backend)-->>BL: new place record
    deactivate Database(Backend)

    BL-->>API: success response
    deactivate BL

    API-->>Owner(Frontend): HTTP Created
    deactivate API
```

```mermaid
sequenceDiagram
    participant Client(Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database(Backend)

    Client(Frontend)->>API: POST /Client/place/review
    activate API
    Note right of API: Client place review request

    API->>BL: reviewPlace(ClientData)
    activate BL

    BL->>Database(Backend): saveReview(ClientData)
    activate Database(Backend)

    Database(Backend)-->>BL: new review record
    deactivate Database(Backend)

    BL-->>API: success response
    deactivate BL

    API-->>Client(Frontend): HTTP Created
    deactivate API
```

```mermaid
sequenceDiagram
    participant Client(Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database(Backend)

    Client(Frontend)->>API: GET /Client/FetchPlace
    activate API
    Note right of API: Client FetchPlace request

    API->>BL: FetchPlace(ClientData)
    activate BL

    BL->>Database(Backend): saveFetchPlace(ClientData)
    activate Database(Backend)

    Database(Backend)-->>BL: new FetchPlace record
    deactivate Database(Backend)

    BL-->>API: success response
    deactivate BL

    API-->>Client(Frontend): HTTP Created
    deactivate API
```
[3. Documentation Compilation:]() The compilation of all diagrams and their explanatory notes into a single, cohesive document. This final document serves as a complete reference for the implementation phase, ensuring the entire development team works from the same architectural vision.

🛠️ Prerequisites
Diagramming Software: Proficiency with a tool like Mermaid.js to create and manage UML diagrams.

UML Knowledge: A basic understanding of UML notation for class, package, and sequence diagrams is required.

# 🚀 Tests
As this project is a documentation and design exercise, there are no tests to run. The expected deliverables are the UML diagrams and the accompanying documentation.

# ✍️ Authors

<div align="center">
  
| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Florian Hadjar** | Co-Developer | [@Boubouche1709](https://github.com/Boubouche1709) | 10482@holbertonstudents.com |
| **Mathieu Godalier** | Co-developer | [@Mathieu7483](https://github.com/Mathieu7483) | 11436@holbertonstudents.com |
</div>

# ⚖️ License
This project is licensed under the MIT License. For more details, see the LICENSE file.
