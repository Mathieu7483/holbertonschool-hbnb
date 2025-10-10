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
        Client-->>Client: Show "Invalid input" message"
    else Valid data
        API->>BL: registerUser(userData)
        activate BL

        alt API validation error
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
            else Duplicate user
                DB-->>BL: error "Duplicate entry"
                Note right of BL: User already exists
                BL-->>API: HTTP 422 Conflict
                API-->>Client: Show "User already exists"
            else Success
                DB-->>BL: new user record
                Note right of BL: User successfully created
                BL-->>API: success response
                API-->>Client: HTTP 201 Created
            end
            deactivate DB
        end
    end

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

    alt Invalid request (Owner -> API)
        Note right of API: Input validation (Frontend)
        API-->>Owner: HTTP 400 Bad Request
    else Valid request
        API->>BL: registerPlace(OwnerData)
        activate BL

        alt Validation or business logic error (API -> BL)
            Note right of BL: Data validation (e.g., missing data)
            BL-->>API: Error: Invalid Data
            API-->>Owner: HTTP 422 Unprocessable Entity
        else Valid data
            BL->>Database: savePlace(OwnerData)
            activate Database

            alt Database error (BL -> Database)
                Note right of Database: Insert failure (e.g., constraint violated)
                Database-->>BL: Error: DB Constraint Violation
                BL-->>API: Error: Database Issue
                API-->>Owner: HTTP 500 Internal Server Error
            else Successful save
                Database-->>BL: new place record
                BL-->>API: success response
                API-->>Owner: HTTP 201 Created
            end
            deactivate Database
        end
        deactivate BL
    end
    deactivate API
```

# 3 - Review Submission
## A user submits a review for a place.
```mermaid
sequenceDiagram
    participant Client as Client (Frontend)
    participant API as HBnB API
    participant BL as Business Logic Layer
    participant Database as Database (Backend)

    Client->>API: POST /client/place/review
    activate API
    Note right of API: Client place review request

    alt Invalid request (Client -> API)
        Note right of API: Input validation (Frontend)
        API-->>Client: HTTP 400 Bad Request
    else Valid request
        API->>BL: reviewPlace(ClientData)
        activate BL

        alt Validation or business logic error (API -> BL)
            Note right of BL: Data validation (e.g., missing rating, invalid place ID)
            BL-->>API: Error: Invalid Data
            API-->>Client: HTTP 422 Unprocessable Entity
        else Valid data
            BL->>Database: saveReview(ClientData)
            activate Database

            alt Database error (BL -> Database)
                Note right of Database: Insert failure (e.g., duplicate review, foreign key violation)
                Database-->>BL: Error: DB Constraint Violation
                BL-->>API: Error: Database Issue
                API-->>Client: HTTP 500 Internal Server Error
            else Successful save
                Database-->>BL: new review record
                BL-->>API: success response
                API-->>Client: HTTP 201 Created
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

    Client->>API: GET /places?location=Paris&price<100
    activate API
    Note right of API: Fetch places with filters

    alt Invalid request (Client -> API)
        Note right of API: Query validation (e.g., invalid filter format)
        API-->>Client: HTTP 400 Bad Request
    else Valid request
        API->>BL: getPlaces(filters)
        activate BL

        alt Validation or business logic error (API -> BL)
            Note right of BL: Filter validation (e.g., unsupported parameters)
            BL-->>API: Error: Invalid Filters
            API-->>Client: HTTP 422 Unprocessable Entity
        else Valid filters
            BL->>Database: queryPlaces(filters)
            activate Database

            alt Database error (BL -> Database)
                Note right of Database: Query failure (e.g., connection timeout, syntax error)
                Database-->>BL: Error: DB Query Failed
                BL-->>API: Error: Database Issue
                API-->>Client: HTTP 500 Internal Server Error
            else Successful query
                Database-->>BL: list of places
                BL-->>API: list of places
                alt No results found
                    Note right of API: Empty result set
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
