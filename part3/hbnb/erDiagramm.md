## 📌 Database Model Overview

This database represents an accommodation booking system with five main entities:

- **User**: Stores personal data and roles.
  - Can own places and write reviews.

- **Place**: Contains listing details (description, price, location).
  - Owned by a user, receives reviews, and includes amenities.

- **Amenity**: Represents features available in places (e.g., Wi-Fi, parking).
  - Linked to places through a many-to-many relationship.

- **Review**: Stores ratings and comments written by users about places.

- **Place_Amenity**: Join table linking places and amenities.

### Relationships
- One user → many places
- One user → many reviews
- One place → many reviews
- Many places ↔ many amenities


```mermaid
erDiagram

    %% === ENTITIES ===
    USER {
        string id PK
        string firstName
        string lastName
        string mail
        string password
        string role
    }

    PLACE {
        string id PK
        string title
        string description
        float price
        float longitude
        float latitude
        string ownerId FK
    }

    AMENITY {
        string id PK
        string name
        string description
    }

    REVIEW {
        string id PK
        int rating
        string comment
        date date
        string clientId FK
        string placeId FK
    }

    PLACE_AMENITY {
        string placeId FK
        string amenityId FK
    }

    %% === RELATIONSHIPS ===

    %% Owner owns many places
    USER ||--o{ PLACE : "owns"

    %% Client writes many reviews
    USER ||--o{ REVIEW : "writes"

    %% A place receives many reviews
    PLACE ||--o{ REVIEW : "receives"

    %% Many-to-Many between Place & Amenity
    PLACE ||--o{ PLACE_AMENITY : "has"
    AMENITY ||--o{ PLACE_AMENITY : "included_in"
```