# HBnB Detailed Class Diagram
This diagram provides a detailed view of the core business entities and their relationships within the HBnB application. It illustrates the attributes and methods of each class, focusing on the Business Logic Layer.

The diagram shows:

Inheritance: How specific user types (Client, Owner, Administrator) inherit from the base User class.

Cardinality: The number of objects involved in each relationship (e.g., a Place can have many Reviews).

Composition & Aggregation: The specific nature of relationships, showing how entities are connected (e.g., a Place is composed of Amenities).

This detailed view is crucial for understanding the object-oriented structure of the application and for guiding the development of the core business logic

```mermaid
classDiagram
    User <|-- Client : *
    User <|-- Administrator : 2 admins Florian et Mathieu
    User <|-- Owner : *
    User : - First name
    User : - Last name
    User: - Mail
    User: - Password
    User: + Register()
    User: + Update()
    User: + Delete()

    class Client{
      -ID
      -
    }
    Client -- PlaceEntity
    class Administrator{
      - Boolean ID
      + Modify()
    }
    Administrator -- Client
    Administrator -- Owner
    Administrator -- PlaceEntity
    Administrator -- AmenityEntity
    Administrator -- ReviewEntity

    class Owner{
      - Boolean ID
      + Create()
      + Update()
      + Delete()
      + Listed()
    }
    class PlaceEntity{
        - Title = Str
        - Descritpion = Str
        - Price = Float
        - Longitude = Float
        - Lattitude = Float
    }
    Owner -- PlaceEntity

    class ReviewEntity{
        - Place = Str
        - User = Str
        - Rating = Int
        - Comment = Str
    }
    ReviewEntity -- Client

    class AmenityEntity{
        - Name = Str
        - Descritpion = Str
        }
    AmenityEntity -- Owner
    AmenityEntity -- PlaceEntity


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
