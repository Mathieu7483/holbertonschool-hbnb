<p align="center">
<img src="https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/Logo%20de%20hippocampe%20et%20circuits%20%C3%A9lectroniques.png" width="1000">
</p>

Project Summary: HBnB Evolution - Technical Documentation (Part 1)
This first part of the HBnB Evolution project focuses on establishing robust technical documentation, which will serve as the detailed blueprint before implementation. The objective is to model the architecture and design of the application, a simplified version of an AirBnB-like service.

The application will manage four main entities: Users, Places, Reviews, and Amenities.

🎯 Core Objectives
The main challenge is to translate the business rules and architecture into clear and precise UML diagrams.


| Entity | Primary Business Rules and Roles | 
| :--- | :--- | 
| **User** | Management (CRUD), unique ID, first\_name, last\_name, email, password, administrator status (boolean).| 
| **Place** | Management (CRUD), title, description, price, latitude, longitude, associated with an owner (User), can have a list of Amenities (Amenity).| 
| **Review** | Management (CRUD), associated with a specific Place and User, includes a rating and a comment.| 
| **Amenity** | Management (CRUD), name, description.|

Common Attributes for all entities: Unique ID, creation and update timestamps.

🧱 Architecture and Modeling Tasks
The application is designed using a Layered Architecture, separated into three levels that communicate via the Facade design pattern:

Presentation Layer: API and services for user interaction.

Business Logic Layer: Data models and core business rules.

Persistence Layer: Responsibility for storing and retrieving data (database).

Required Diagrams and Documentation:
| Task | Description of Output |
| :--- | :--- |
| **High-Level Package Diagram** | Overview illustrating the 3 architectural layers and their communication via the **Facade** pattern. |
| **Detailed Class Diagram** | Modeling the User, Place, Review, and Amenity entities within the Business Logic Layer, including attributes, methods, and their relationships (notably between Place and Amenity). |
| **Sequence Diagrams** | Representation of the information flow (interactions between the 3 layers) for at least four API calls: **user registration**, **place creation**, **review submission**, and **fetching a list of places**. |
| **Documentation Compilation** | Gathering all diagrams and explanatory notes into a coherent technical document. |

✔️ Conditions and Constraints
-Mandatory use of UML notation for all diagrams.

-Accurate representation of business rules in the diagrams.

-Diagrams must serve as a detailed guide for future implementation.

This work ensures a clear understanding and a precise plan before moving on to the implementation phases.

# 📝 Description Part 1
This project, HBnB Evolution, is the initial phase of developing a simplified AirBnB-like application. This part focuses on creating a comprehensive technical documentation blueprint using UML (Unified Modeling Language). The goal is to design the system's architecture and interactions before implementation, ensuring a clear and shared understanding among the team. The application is structured into three main layers: the Presentation Layer, the Business Logic Layer, and the Persistence Layer.

# 📂 Exercise Content
This directory contains the UML diagrams and explanatory notes that form the technical documentation for the project.

[0. High-Level Package Diagram:](https://github.com/Mathieu7483/holbertonschool-hbnb/blob/Mathieu/part1/high%20package%20level%20diagram.md) A high-level package diagram illustrating the application's three-layer architecture and the communication between them via the Facade Pattern. This diagram provides an overview of the code's organization.

[1. Detailed Class Diagram for Business Logic Layer:](https://github.com/Mathieu7483/holbertonschool-hbnb/blob/Mathieu/part1/detailed%20classes%20diagram.md) A detailed class diagram for the Business Logic layer. It models the core entities of the application (User, Place, Review, Amenity) with their attributes, methods, and relationships. This diagram is crucial for designing the data models.

[2. Sequence Diagrams for API Calls:](https://github.com/Mathieu7483/holbertonschool-hbnb/blob/Mathieu/part1/Sequence%20Diagrams%20for%20API%20Calls.md) A series of sequence diagrams that illustrate the flow of information and interactions between the different layers for specific use cases, such as user registration, place creation, review submission, and fetching a list of places.

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
