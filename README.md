<p align="center">
<img src="https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/Logo%20de%20hippocampe%20et%20circuits%20%C3%A9lectroniques.png" width="1000">
</p>



# 📝 Description Part 1
This project, HBnB Evolution, is the initial phase of developing a simplified AirBnB-like application. This part focuses on creating a comprehensive technical documentation blueprint using UML (Unified Modeling Language). The goal is to design the system's architecture and interactions before implementation, ensuring a clear and shared understanding among the team. The application is structured into three main layers: the Presentation Layer, the Business Logic Layer, and the Persistence Layer.

# 📂 Exercise Content
This directory contains the UML diagrams and explanatory notes that form the technical documentation for the project.

[0. High-Level Package Diagram:](https://github.com/Mathieu7483/holbertonschool-hbnb/blob/main/part1/high%20package%20level%20diagram.md) A high-level package diagram illustrating the application's three-layer architecture and the communication between them via the Facade Pattern. This diagram provides an overview of the code's organization.

[1. Detailed Class Diagram for Business Logic Layer:](https://github.com/Mathieu7483/holbertonschool-hbnb/blob/main/part1/detailed%20classes%20diagram.md) A detailed class diagram for the Business Logic layer. It models the core entities of the application (User, Place, Review, Amenity) with their attributes, methods, and relationships. This diagram is crucial for designing the data models.

[2. Sequence Diagrams for API Calls:](https://github.com/Mathieu7483/holbertonschool-hbnb/blob/main/part1/Sequence%20Diagrams%20for%20API%20Calls.md) A series of sequence diagrams that illustrate the flow of information and interactions between the different layers for specific use cases, such as user registration, place creation, review submission, and fetching a list of places.

[3. Documentation Compilation:](https://github.com/Mathieu7483/holbertonschool-hbnb/blob/main/part1/HBnB_Description_Notes.md) The compilation of all diagrams and their explanatory notes into a single, cohesive document. This final document serves as a complete reference for the implementation phase, ensuring the entire development team works from the same architectural vision.

🛠️ Prerequisites
Diagramming Software: Proficiency with a tool like Mermaid.js to create and manage UML diagrams.

UML Knowledge: A basic understanding of UML notation for class, package, and sequence diagrams is required.

# 🚀 Tests
As this project is a documentation and design exercise, there are no tests to run. The expected deliverables are the UML diagrams and the accompanying documentation

# 📝 Description Part 2
This second part of the HBnB project marks the beginning of the implementation phase of the application. After defining the architecture and design in the first stage, the objective here is to bring the software structure to life by developing the presentation layer (API) and the business logic layer using Python and the Flask framework, along with the flask-restx extension.
This project follows a modular structure to ensure maintainability and scalability. The current setup implements the foundation for the Business Logic Layer (BLL), the API, and the in-memory persistence layer.

## 🎯 Objectives and Tasks

### 1. Set Up the Project Structure
- Organize the project into a **modular architecture**, following Python and Flask best practices.
- Create packages for the **Presentation** and **Business Logic** layers.

### 2. Implement the Business Logic Layer
- Develop core classes for the business entities:
  `User`, `Place`, `Review`, and `Amenity`.
- Define **relationships** and **interactions** between entities.
- Apply the **Facade Design Pattern** to simplify communication between layers.

### 3. Build RESTful API Endpoints
- Implement **CRUD** (Create, Read, Update, Delete) operations for all entities.
- Use **flask-restx** to define, document, and organize the API.
- Implement **data serialization** to include extended attributes (e.g., a `Place` should include the owner’s details and related amenities).

### 4. Test and Validate the API
- Test endpoints using tools like **Postman** or **cURL**.
- Validate correct behavior and handle edge cases gracefully.

## 🧠 Project Vision and Scope
This implementation focuses on creating a **functional and scalable foundation** for the HBnB application.

### **Presentation Layer**
- Define services and endpoints using **Flask** and **flask-restx**.
- Ensure clear and logical API paths and parameters.

### **Business Logic Layer**
- Build the core models and logic driving the application.
- Handle **data validation**, **relationships**, and **entity interactions**.


# 📝 Description Part 3
In Part 3 of the HBnB Project, the backend is strengthened with user authentication, authorization, and persistent database storage. Using Flask-JWT-Extended, the system now supports JWT-based authentication and role-based access control to secure API endpoints.
To further enhance security, passwords are hashed using bcrypt before being stored in the database. This prevents plain-text password storage and protects user credentials in case of a data breach.
The application moves from in-memory storage to a SQLAlchemy-managed relational database, using SQLite for development and preparing MySQL for production. All CRUD operations are refactored to ensure reliable data persistence.
The project also focuses on defining clear relationships between entities such as users, places, reviews, and amenities. These relationships are modeled and visualized with mermaid.js to ensure proper data linking and consistency across the system.
This phase makes the backend more secure, scalable, and production-ready, providing a solid foundation for real-world deployment.

## 🎯 Objectives and Tasks
## 🧩 Project Tasks Summary — HBnB Part 3

### 🧱 **0. Modify the Application Factory to Include Configuration**
Implement the Flask **Application Factory pattern** to initialize the app using different configuration objects (development, testing, production).
**✅ Outcome:**  
A fully functional `create_app()` method that loads configuration settings dynamically.

### 🔐 **1. Modify the User Model to Include Password Hashing**
Enhance the `User` model to store **hashed passwords** using **bcrypt**.  
Update the registration endpoint to hash the password before saving and never return it in GET requests.
**✅ Outcome:**  
Secure password storage and improved user registration process.

### 🔑 **2. Implement JWT Authentication with `flask-jwt-extended`**
Set up **JWT-based authentication** to manage secure login and token verification.  
Users receive a token on login and use it to access protected API endpoints.
**✅ Outcome:**  
JWT tokens are generated, verified, and embedded with user role claims for secure access control.

### 🧍‍♂️ **3. Implement Authenticated User Access Endpoints**
Secure specific API endpoints to restrict actions like creating or modifying places and reviews to **authenticated users only**.  
Implement ownership validation to ensure users can only edit or delete their own data.
**✅ Outcome:**  
Authenticated users can manage their own resources; public endpoints remain open.

### 🧑‍💼 **4. Implement Administrator Access Endpoints**
Add **role-based access control (RBAC)** so administrators can manage all users, amenities, and resources.  
Admins can bypass ownership restrictions and modify any user’s details.
**✅ Outcome:**  
Admins have full privileges to manage any resource; regular users remain limited to their data.

### 🗄️ **5. Implement SQLAlchemy Repository**
Replace the in-memory data layer with a **SQLAlchemy-based repository**.  
Refactor the Facade and repositories to handle CRUD operations via SQLAlchemy.
**✅ Outcome:**  
Data persistence is now managed by SQLAlchemy, preparing for full ORM integration.

### 👤 **6. Map the User Entity to SQLAlchemy Model**
Map the `User` entity to a SQLAlchemy model with attributes like `first_name`, `last_name`, `email`, `password`, and `is_admin`.  
Ensure password hashing remains functional and integrate it into the repository layer.
**✅ Outcome:**  
Users are fully persisted in the database with ORM support.

### 🏠 **7. Map the Place, Review, and Amenity Entities**
Create SQLAlchemy models for `Place`, `Review`, and `Amenity` with their basic attributes.  
No relationships are added at this stage.
**✅ Outcome:**  
Core entities are mapped to the database and ready for relational setup.

### 🔗 **8. Map Relationships Between Entities Using SQLAlchemy**
Define **one-to-many** and **many-to-many** relationships between `User`, `Place`, `Review`, and `Amenity`.  
Add foreign keys and bidirectional relationships to ensure referential integrity.
**✅ Outcome:**  
All entities are properly linked, enabling relational queries and data consistency.

### 💾 **9. SQL Scripts for Table Generation and Initial Data**
Create raw **SQL scripts** to generate all database tables and relationships, and populate initial data (admin user, amenities, etc.).
**✅ Outcome:**  
SQL schema creation and seed data scripts ready for database initialization.

### 🧭 **10. Generate Database Diagrams**
Use **Mermaid.js** to create **Entity-Relationship (ER) diagrams** representing all tables and their relationships.  
Include these diagrams in the project documentation.
**✅ Outcome:**  
ER diagrams visually represent the complete database structure, aiding understanding and maintenance.

## 🏁 **Final Outcome**
After completing all tasks, the HBnB backend becomes a **secure, scalable, and persistent Flask application** with:

- 🔧 Configuration management  
- 🔒 Secure password storage  
- 🪪 JWT authentication and role-based access control  
- 🗃️ SQLAlchemy ORM persistence  
- 🧠 Clear database documentation with SQL scripts and ER diagrams

# 📝 Description Part 4

# ✍️ Authors

<div align="center">

| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Florian Hadjar** | Co-Developer | [@Boubouche1709](https://github.com/Boubouche1709) | 10482@holbertonstudents.com |
| **Mathieu Godalier** | Co-developer | [@Mathieu7483](https://github.com/Mathieu7483) | 11436@holbertonstudents.com |
</div>

# ⚖️ License
This project is licensed under the MIT License. For more details, see the LICENSE file.
