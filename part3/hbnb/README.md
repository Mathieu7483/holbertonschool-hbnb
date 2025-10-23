Acknowledged, Mathieu. I will now respond **in English** and will keep in mind that you are collaborating with **Florian HADJAR** on the **HBnB - Auth & DB** project.

Here is the revised `README.md` for Part 3 of your HBnB project.

-----

\<p align="center"\>
\<img src="[https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/HBnB%20V2%20Auth%20DB.png](https://www.google.com/search?q=https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/HBnB%2520V2%2520Auth%2520DB.png)"\>
\</p\>

# HBnB Project - Part 3: Enhanced Backend with Authentication and Database Integration

-----

### 📝 **Project Overview**

This third iteration of the HBnB project transforms the backend architecture from a memory-based prototype into a **secure, persistent, and production-ready** system.

In collaboration with **Florian HADJAR**, we focused on integrating two critical components:

1.  **Authentication & Authorization (Auth)**: Securing the API using the **JWT** (JSON Web Token) standard and implementing **Role-Based Access Control (RBAC)** to manage user privileges.
2.  **Database Persistence (DB)**: Replacing the in-memory data store with a relational database layer using the **SQLAlchemy ORM**. We implemented a dual-stack configuration: **SQLite** for development and **MySQL** for production environments.

This phase establishes a robust foundation, ensuring data integrity, scalability, and secure user management.

-----

### 🧑‍💻 **Collaborators**

This project was developed by:

  * **Mathieu GODALIER**
  * **Florian HADJAR**

-----

### 🎯 **Learning Objectives and Achieved Skills**

This project demonstrates proficiency in integrating **Python OOP** and **Flask** with modern database and security services.

#### **I. Security and Access Control**

  * Configuring the Flask **Application Factory** to handle different environments (Dev/Prod).
  * Implementing **password hashing** using `Flask-Bcrypt` to securely store user credentials.
  * Integrating **stateless authentication** using **`Flask-JWT-Extended`** (JWTs).
  * Enforcing **Role-Based Access Control (RBAC)**: Distinguishing admin privileges (`is_admin`) to bypass ownership checks and manage system resources (e.g., Amenities).
  * Implementing **ownership validation** logic for authenticated users (ensuring users can only modify their own Places/Reviews).

#### **II. ORM and Data Persistence**

  * Adopting the **Repository Pattern** with **SQLAlchemy** to decouple database operations from business logic.
  * Mapping all core entities (**`User`**, **`Place`**, **`Review`**, **`Amenity`**) to SQLAlchemy models.
  * Defining **relational mappings** (One-to-Many, Many-to-Many) using `ForeignKey` and `relationship()`.
  * Implementing full **CRUD operations** through the SQLAlchemy Repository.
  * Preparing **raw SQL scripts** (DDL) to understand and define the database schema independently of the ORM.

#### **III. Technical Documentation**

  * Creating **Entity-Relationship (ER) Diagrams** using **Mermaid.js** to visually document the database structure.

-----

### 📁 **Core Tasks Breakdown**

The project progression moved logically from security implementation to full database integration.

#### **Phase 1: Security and Authentication (Tasks 0-4)**

| Task | Objective | Key Implementation |
| :--- | :--- | :--- |
| **0.** App Factory Config | Prepare the application for multi-environment configuration. | `create_app(config_object)` pattern. |
| **1.** Password Hashing | Securely store user passwords. | `Flask-Bcrypt`, `generate_password_hash`, `check_password_hash`. |
| **2.** JWT Auth | Implement secure login and token issuance. | `Flask-JWT-Extended`, `@jwt_required`. |
| **3.** Authenticated Access | Protect endpoints and enforce resource ownership. | Ownership checks using JWT identity and database query. |
| **4.** Administrator Access | Implement admin privileges. | RBAC logic based on `is_admin` claim in the JWT payload. |

#### **Phase 2: ORM and Persistence (Tasks 5-8)**

| Task | Objective | Key Implementation |
| :--- | :--- | :--- |
| **5.** SQLAlchemy Repository | Replace in-memory storage with an ORM-based layer. | **`SQLAlchemyRepository`** implementing the repository interface. |
| **6.** Map User Entity | Map the `User` class to a database table. | SQLAlchemy **Declarative Base**, `Column`, `relationship`. |
| **7.** Map Core Entities | Map `Place`, `Review`, and `Amenity`. | Model definition using standard attributes and data types. |
| **8.** Map Relationships | Define how entities are connected. | `ForeignKey` and `relationship()` with appropriate `backref` definitions. |

#### **Phase 3: Schema & Documentation (Tasks 9-10)**

| Task | Objective | Key Implementation |
| :--- | :--- | :--- |
| **9.** SQL Scripts | Ensure foundational knowledge of pure SQL DDL/DML. | Creation of all table structures and initial data (admin, amenities). |
| **10.** Generate Diagrams | Visually represent the final database schema. | **Mermaid.js** syntax for ER diagrams. |

-----

### 🛠️ **Technologies & Dependencies**

  * **Language** : Python 3.8+
  * **Framework** : Flask
  * **ORM** : SQLAlchemy
  * **Security** : `Flask-JWT-Extended`, `Flask-Bcrypt`
  * **Database (Dev)** : SQLite
  * **Database (Prod)** : MySQL

-----

# ✍️ Authors

<div align="center">

| Author | Role | GitHub | Email |
|--------|------|--------|-------|
| **Florian Hadjar** | Co-Developer | [@Boubouche1709](https://github.com/Boubouche1709) | 10482@holbertonstudents.com |
| **Mathieu Godalier** | Co-developer | [@Mathieu7483](https://github.com/Mathieu7483) | 11436@holbertonstudents.com |
</div>

# ⚖️ License
This project is licensed under the MIT License. For more details, see the LICENSE file.