<p align="center">
<img src="https://github.com/Mathieu7483/Aiko78-Photgraphy/blob/main/img/Logo%20de%20hippocampe%20et%20circuits%20%C3%A9lectroniques.png" width="1000">
</p>

-----

# 🌐 HBnB - Simple Web Client (Part 4: Front-end)

-----

## 📝 Project Description

This project constitutes Phase 4 of the **HBnB** application development, focusing on the creation of a **Simple Web Client (Front-end)**. It implements an interactive user interface using **HTML5, CSS3, and JavaScript ES6** to communicate with the previously developed back-end API.

The technical objective is to build a **dynamic and responsive** web application that handles navigation, user authentication via a **JWT** stored in a **cookie**, displays data (list and details of places), client-side filtering, and form submission, all while utilizing **AJAX** technology (Fetch API) to prevent full page reloads.

-----

## 💻 Exercise Content

This repository contains the foundational HTML and CSS files, along with the JavaScript scripts implementing the client-side behavior for the HBnB application.

| File | Objective | Role |
| :--- | :--- | :--- |
| **`login.html`** | **User Authentication** | Contains the login form. The associated script manages form submission, the API login call, and the storage of the **JWT** in a **cookie** for session management. |
| **`index.html`** | **List of Places** | Main page displaying all available places. The script handles authentication checks, API calls to fetch data, dynamic rendering of place cards (`place-card`), and the implementation of a client-side **price filter**. |
| **`place.html`** | **Place Details** | Displays detailed information for a specific place, including amenities and reviews. The script extracts the Place ID from the URL and only displays the review submission form (`add-review`) if the user is authenticated. |
| **`add_review.html`** | **Review Form** | Form allowing authenticated users to add a new review for a place. The script ensures only authenticated users can access the form and handles the `POST` API call for data submission. |
| **`scripts.js`** | **Client-side Logic** | Contains all JavaScript ES6 functions for DOM manipulation, cookie handling (for JWT), `fetch` calls to API endpoints (Login, Places, Reviews), and redirection logic. |
| **`style.css`** | **Application Styling** | CSS3 file containing necessary styles, adhering to layout constraints and required classes (`place-card`, `details-button`, etc.) |

-----

## ⚙️ Prerequisites

To run and test this web client, the following dependencies are required:

### 🛠️ Dependencies

1.  **Functional HBnB API:** The back-end developed in previous parts of the project must be running and accessible.
2.  **CORS Configuration:** The Flask API must be configured to allow **Cross-Origin Resource Sharing (CORS)** requests originating from the web client's host (e.g., `http://127.0.0.1:8000`).
3.  **Web Browser:** A modern browser compatible with **JavaScript ES6** and the **Fetch API** (Chrome, Firefox, Safari, etc.).

### ⚠️ Note on CORS

If you encounter `Cross-Origin` security errors, you must modify your Flask API code to include the appropriate CORS headers or use an extension like `flask-cors`.

-----

## 🚀 Usage and Execution

Since this is a web client, no "compilation" is necessary. Execution is performed directly in the browser.

1.  **Start the API:**

      * Ensure your HBnB Flask application is running (typically on port 5000).

      ```bash
      #example launch server
      ~/Holberton/holbertonschool-hbnb/part3/hbnb$ python3 run.py
      ```

2.  **Launch the Web Client:**

      * Open the `index.html` file in your web browser.
      * **Recommendation:** Use a simple local web server (such as **Python's `http.server`**) to avoid browser security restrictions when making AJAX calls (the `file://` protocol).

<!-- end list -->

```bash
# Example launch using Python's http.server module
cd ~/Holberton/holbertonschool-hbnb/part4
python3 -m http.server 8000
# The web client is accessible via: http://localhost:8000/index.html
```

3.  **Test Authentication:**
      * Navigate to `login.html`.
      * Log in with valid credentials to obtain the JWT stored in the cookies.
      * Verify the `token` cookie in the browser's developer tools.

-----
# Snippet video

[Here the video link](https://youtu.be/hjov5nvEGNo)

-----

# ✍️ Authors

[Mathieu GODALIER](https://github.com/Mathieu7483) - Holberton school's student 

# ⚖️ License
This project is licensed under the MIT License. For more details, see the LICENSE file.
