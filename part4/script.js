// API endpoint URL for login
const API_LOGIN_URL = 'https://part3/hbnb/app/api/v2/auth/login'; 

// 1. Handles the AJAX request (Fetch API) to the login endpoint
async function loginUser(email, password) {
    try {
        const response = await fetch(API_LOGIN_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        return response;
    } catch (error) {
        console.error("Error during login request:", error);
        // Return a mock error response to be handled by the listener's catch block
        return { ok: false, statusText: 'Network Error' }; 
    }
}

// 2. DOMContentLoaded event and form submission handling
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        // Add event listener for form submission
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                // Call the function to make the API request
                const response = await loginUser(email, password);

                // 3. Handle the API response (Success/Failure)
                if (response.ok) {
                    const data = await response.json();
                    
                    // Store the JWT token in a cookie and redirect
                    document.cookie = `token=${data.access_token}; path=/; max-age=3600; secure; samesite=Lax`; 
                    window.location.href = 'index.html';
                } else {
                    // If response is not 201, show an error message
                    const errorData = response.statusText ? response.statusText : (await response.json()).error;
                    alert('Login failed: ' + errorData);
                }
            } catch (error) {
                console.error('Unrecoverable error during login process:', error);
                alert('An error occurred. Please try again later.');
            }
        });
    }
});