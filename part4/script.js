// API endpoint URLs
const API_BASE_URL = 'http://localhost:5000';
const API_LOGIN_URL = `${API_BASE_URL}/api/v2/auth/login`;
const API_PLACES_URL = `${API_BASE_URL}/api/v2/places`;

// ==================== COOKIE HELPER FUNCTIONS ====================

// Helper function to set a cookie
function setCookie(name, value, maxAge = 3600) {
    document.cookie = `${name}=${value}; path=/; max-age=${maxAge}; SameSite=Lax`;
}

// Helper function to get a cookie value by its name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Helper function to delete a cookie
function deleteCookie(name) {
    document.cookie = `${name}=; path=/; max-age=0`;
}

// ==================== LOGIN FUNCTIONALITY ====================

// Handles the AJAX request (Fetch API) to the login endpoint
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
        throw error;
    }
}

// ==================== AUTHENTICATION CHECK ====================

// Check if user is authenticated and update UI accordingly
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        // User is NOT authenticated
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
    } else {
        // User IS authenticated
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';
        
        // Fetch places data if we're on the index page
        const placesList = document.getElementById('places-list');
        if (placesList) {
            fetchPlaces(token);
        }
    }
}

// ==================== FETCH PLACES FUNCTIONALITY ====================

// Global variable to store all places for filtering
let allPlaces = [];

// Fetch places data from API
async function fetchPlaces(token) {
    try {
        const response = await fetch(API_PLACES_URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const places = await response.json();
            allPlaces = places; // Store for filtering
            displayPlaces(places);
        } else {
            if (response.status === 401) {
                // Token is invalid or expired
                alert('Your session has expired. Please login again.');
                deleteCookie('token');
                window.location.href = 'login.html';
            } else {
                console.error('Failed to fetch places:', response.statusText);
                const placesList = document.getElementById('places-list');
                if (placesList) {
                    placesList.innerHTML = '<p>Failed to load places. Please try again later.</p>';
                }
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        const placesList = document.getElementById('places-list');
        if (placesList) {
            placesList.innerHTML = '<p>Network error. Please check your connection.</p>';
        }
    }
}

// ==================== DISPLAY PLACES FUNCTIONALITY ====================

// Display places in the DOM
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    
    if (!placesList) return;

    // Clear current content
    placesList.innerHTML = '';

    // Check if there are places to display
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
        return;
    }

    // Iterate over places and create elements
    places.forEach(place => {
        const placeCard = document.createElement('article');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price_per_night || 0; // Store price for filtering

        placeCard.innerHTML = `
            <h2>${place.name || 'Unnamed Place'}</h2>
            <div class="place-price">Price: $${place.price_per_night || 0}/night</div>
            <div class="place-location">${place.city || ''}, ${place.country || ''}</div>
            <p class="place-description">${place.description || 'No description available.'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

// ==================== PRICE FILTERING FUNCTIONALITY ====================

// Filter places by price
function filterPlacesByPrice(maxPrice) {
    let filteredPlaces;

    if (maxPrice === 'all') {
        filteredPlaces = allPlaces;
    } else {

        filteredPlaces = allPlaces.filter(place => {
            const price = parseFloat(place.price_per_night) || 0;
            return price <= maxPrice;
        });
    }

    displayPlaces(filteredPlaces); 
}

// ==================== DOM CONTENT LOADED ====================

document.addEventListener('DOMContentLoaded', () => {
    // Check authentication on page load
    checkAuthentication();

    // ========== LOGIN FORM HANDLING ==========
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            // Basic validation
            if (!email || !password) {
                alert('Please enter both email and password.');
                return;
            }

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    
                    // Store JWT token in cookie (1 hour expiration)
                    setCookie('token', data.access_token, 3600);
                    
                    // Redirect to main page
                    window.location.href = 'index.html';
                } else {
                    let errorMessage = 'Login failed. ';
                    
                    if (response.status === 401) {
                        errorMessage += 'Invalid email or password.';
                    } else if (response.status === 400) {
                        errorMessage += 'Please check your input.';
                    } else if (response.status >= 500) {
                        errorMessage += 'Server error. Please try again later.';
                    } else {
                        try {
                            const errorData = await response.json();
                            errorMessage += errorData.message || errorData.error || response.statusText;
                        } catch {
                            errorMessage += response.statusText;
                        }
                    }
                    
                    alert(errorMessage);
                }
            } catch (error) {
                console.error('Unrecoverable error during login process:', error);
                alert('Network error. Please check your connection and try again.');
            }
        });
    }

    // ========== LOGOUT BUTTON HANDLING ==========
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            deleteCookie('token');
            window.location.href = 'login.html';
        });
    }

    // ========== PRICE FILTER HANDLING ==========
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            filterPlacesByPrice(event.target.value);
        });
            
            // Convert filter value to max price
            let maxPrice;
            switch(selectedValue) {
                case '10':
                    maxPrice = 10;
                    break;
                case '50':
                    maxPrice = 50;
                    break;
                case '100':
                    maxPrice = 100;
                    break;
                case 'all':
                default:
                    maxPrice = 'all';
                    break;
            }
            
            filterPlacesByPrice(maxPrice);
        }
});