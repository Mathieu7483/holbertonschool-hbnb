# Sequence Diagrams for API Calls

# 1 - User Registration
## A user signs up for a new account.
```mermaid
sequenceDiagram
    participant Client as Frontend
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant DB as Database (Backend)

    Client->>API: POST /users/register
    activate API
    Note right of API: User registration request

    alt Invalid form data (frontend validation failed)
        Client-->>Client: Show "Invalid input" message
    else Valid data
        API->>BL: registerUser(userData)
        activate BL

        alt API validation error (bad format, missing fields)
            BL-->>API: Validation failed
            API-->>Client: HTTP 400 Bad Request
            Note left of Client: Display validation error
        else Valid request
            BL->>DB: saveUser(userData)
            activate DB

            alt Database unreachable
                DB-->>BL: error "Connection timeout"
                Note right of BL: Database unreachable
                BL-->>API: HTTP 500 Internal Server Error
                API-->>Client: Show "Service unavailable"
            else Duplicate user (email or id already exists)
                DB-->>BL: error "Duplicate entry"
                Note right of BL: User already exists
                BL-->>API: HTTP 409 Conflict
                API-->>Client: Show "User already exists"
            else Success
                DB-->>BL: new user record
                Note right of BL: User successfully created
                BL-->>API: HTTP 201 Created
                API-->>Client: Show "User created successfully"
            end
            deactivate DB
        end
    end

    deactivate BL
    deactivate API

    %% Additional GET /users/{id} scenario for 404
    Client->>API: GET /users/{id}
    activate API
    API->>BL: getUser(userId)
    activate BL
    BL->>DB: findUser(userId)
    activate DB

    alt User not found
        DB-->>BL: null
        BL-->>API: HTTP 404 Not Found
        API-->>Client: Show "User not found"
    else Success
        DB-->>BL: user data
        BL-->>API: HTTP 200 OK
        API-->>Client: Return user data (no password)
    end
    deactivate DB
    deactivate BL
    deactivate API
```


# 2 - Place Creation
## A user creates a new place listing.
```mermaid
sequenceDiagram
    participant Owner as Owner (Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database as Database (Backend)

    Owner->>API: POST /owner/place/register
    activate API
    Note right of API: Owner place registration request

    alt Invalid request (frontend validation failed)
        Note right of API: Input validation
        API-->>Owner: HTTP 400 Bad Request
        Note left of Owner: Show "Invalid input"
    else Valid request
        API->>BL: registerPlace(placeData)
        activate BL

        alt Validation or business logic error
            Note right of BL: Missing fields or invalid data
            BL-->>API: Error: Invalid Data
            API-->>Owner: HTTP 422 Unprocessable Entity
            Note left of Owner: Show "Invalid data"
        else Valid data
            BL->>Database: savePlace(placeData)
            activate Database

            alt Database unreachable
                Database-->>BL: Error: Connection timeout
                BL-->>API: HTTP 500 Internal Server Error
                API-->>Owner: Show "Service unavailable"
            else Duplicate place (title + owner)
                Database-->>BL: Error: Duplicate entry
                BL-->>API: HTTP 409 Conflict
                API-->>Owner: Show "Place already exists"
            else Success
                Database-->>BL: new place record
                BL-->>API: Success response
                API-->>Owner: HTTP 201 Created
                Note left of Owner: Show "Place created successfully"
            end
            deactivate Database
        end
        deactivate BL
    end
    deactivate API
```


# 3 - Review Submission
## A user submits a review for a place
```mermaid
sequenceDiagram
    participant Client as Client (Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database as Database (Backend)

    Client->>API: POST /client/place/review
    activate API
    Note right of API: Client place review request

    alt Invalid request (frontend validation failed)
        Note right of API: Input validation (missing rating, comment, invalid placeId)
        API-->>Client: HTTP 400 Bad Request
        Note left of Client: Show "Invalid input"
    else Valid request
        API->>BL: reviewPlace(reviewData)
        activate BL

        alt Validation or business logic error
            Note right of BL: Missing fields, invalid rating, non-existent place
            BL-->>API: Error: Invalid Data
            API-->>Client: HTTP 422 Unprocessable Entity
            Note left of Client: Show "Invalid data"
        else Valid data
            BL->>Database: saveReview(reviewData)
            activate Database

            alt Database unreachable
                Database-->>BL: Error: Connection timeout
                BL-->>API: HTTP 500 Internal Server Error
                API-->>Client: Show "Service unavailable"
            else Duplicate review (same client & place)
                Database-->>BL: Error: Duplicate entry
                BL-->>API: HTTP 409 Conflict
                API-->>Client: Show "Review already exists"
            else Place not found
                Database-->>BL: Error: Foreign key violation
                BL-->>API: HTTP 404 Not Found
                API-->>Client: Show "Place not found"
            else Success
                Database-->>BL: new review record
                BL-->>API: Success response
                API-->>Client: HTTP 201 Created
                Note left of Client: Show "Review created successfully"
            end
            deactivate Database
        end
        deactivate BL
    end
    deactivate API
```

# 4 - Fetching a list of places
## A user requests a list of places based on certain criteria.
```mermaid
sequenceDiagram
    participant Client as Client (Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database as Database (Backend)

    %% --- Fetch a single place ---
    Client->>API: GET /places/{id}
    activate API
    Note right of API: Fetch place by ID

    alt Invalid request (malformed ID)
        API-->>Client: HTTP 400 Bad Request
        Note left of Client: Show "Invalid request"
    else Valid request
        API->>BL: getPlaceById(placeId)
        activate BL

        alt Validation or business logic error
            BL-->>API: Error: Invalid ID format
            API-->>Client: HTTP 422 Unprocessable Entity
        else Valid ID
            BL->>Database: findPlaceById(placeId)
            activate Database

            alt Place not found
                Database-->>BL: null
                BL-->>API: HTTP 404 Not Found
                API-->>Client: Show "Place not found"
            else Success
                Database-->>BL: place data
                BL-->>API: place data
                API-->>Client: HTTP 200 OK + place
            end
            deactivate Database
        end
        deactivate BL
    end
    deactivate API

    %% --- Fetch multiple places with filters ---
    Client->>API: GET /places?location=Paris&price<100
    activate API
    Note right of API: Fetch places with filters

    alt Invalid request (Client -> API)
        API-->>Client: HTTP 400 Bad Request
    else Valid request
        API->>BL: getPlaces(filters)
        activate BL

        alt Validation or business logic error
            BL-->>API: Error: Invalid Filters
            API-->>Client: HTTP 422 Unprocessable Entity
        else Valid filters
            BL->>Database: queryPlaces(filters)
            activate Database

            alt Database error
                Database-->>BL: Error: DB Query Failed
                BL-->>API: HTTP 500 Internal Server Error
            else Successful query
                Database-->>BL: list of places
                BL-->>API: list of places
                alt No results found
                    API-->>Client: HTTP 200 OK + []
                else Results found
                    API-->>Client: HTTP 200 OK + [places...]
                end
            end
            deactivate Database
        end
        deactivate BL
    end
    deactivate API
```
